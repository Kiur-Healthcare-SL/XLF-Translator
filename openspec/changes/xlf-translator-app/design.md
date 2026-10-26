# Design

## Context

Greenfield project; no code exists. See proposal.md for motivation.

The two `ace-app` catalogs (360 units, source language `es`) were measured to
learn what real Angular catalogs contain: inline placeholders in about 8% of
units, up to 10 in one unit, often paired (`<b>`...`</b>`, a button wrapping a
`<mat-icon>`); leading and trailing whitespace, some of it non-breaking; escaped
HTML as literal text up to 974 characters; one whitespace-only source; targets
identical to their source; and, in the shipped en-GB file, two units whose
placeholders were all deleted. Those catalogs are **not** used as fixtures.
Synthetic fixtures with the same profile are written for an imaginary CT-scan
(TAC) analysis app; see D14.

The architectural and style constraints are fixed by the project configuration
and are treated here as given, not re-argued.

## Goals / Non-Goals

**Goals:**
- Make placeholder loss impossible to export, whether typed or imported.
- Keep every business rule testable without importing Streamlit.
- Keep every element and attribute the translator does not edit, including
  `<note>` and `<context-group>`.

**Non-Goals:**
- Byte-for-byte equality with the uploaded file. Attribute quoting, the XML
  declaration and similar formatting may change; content may not.
- Machine translation and signature embedding (deferred).
- XLIFF 2.x, multi-`<file>` documents, ICU plural or select messages, and any
  encoding other than UTF-8.
- Concurrent or multi-user editing. One browser session, one catalog.

## Decisions

### D1 — Masking is a domain rule, not a display trick

`{n}` tokens never reach disk; they exist only between parse and serialise.
Because the safety argument rests on them, masking lives in **domain**, and is
exercised by a round-trip test over every fixture unit before any UI exists.

Alternative considered: let the translator edit raw `<x .../>` XML. Rejected —
a malformed fragment cannot be parsed, so the app could not name which
placeholder was lost.

### D2 — Layer assignment

| Concept | Layer |
| --- | --- |
| `TranslationUnit`, `UnitIdentifier`, `SourceContent`, `TargetContent` | domain |
| `Placeholder`, `PlaceholderName`, `PlaceholderAttributes`, `PlaceholderToken`, `Content`, `ContentMask`, `ContentUnmask`, `PlaceholderComparison` | domain |
| `Catalog` (first-class collection of units), `CatalogPosition`, `CatalogClassification`, `CompletionReport`, `AutoFillReport` | domain |
| `LanguageCode`, `LanguagePair`, `ArtifactName` | domain |
| `UploadedDocument` (stem and bytes), `DocumentSize` | domain |
| `TranslationSession` (position within catalog, target language) | domain |
| `CatalogRefusal` | domain |
| `OpenDocument` (uploaded document and session) | application |
| `OpenCatalog`, `ChooseTargetLanguage`, `MoveToUnit`, `EnterTarget`, `CopySourceIntoTarget`, `ExportDraft`, `ExportFinal` | application |
| `UnitView`, `SessionView` and their builders | application |
| `CatalogReader`, `CatalogWriter`, `SessionRepository` (ports) | application |
| `ElementTreeCatalogReader`, `ElementTreeCatalogWriter` | infrastructure |
| `SessionStateSessionRepository` | presentation (implements an application port) |
| Screens, language form, widgets, whitespace markup, download buttons | presentation |

### D3 — Ports and their implementations

- `CatalogReader` — takes an `UploadedDocument`, answers a `Catalog` with its
  `LanguagePair`, or a `CatalogRefusal`. Implemented by
  `ElementTreeCatalogReader` (infrastructure).
- `CatalogWriter` — takes the original `UploadedDocument`, the `Catalog` and the
  target `LanguageCode`, answers document bytes. Implemented by
  `ElementTreeCatalogWriter` (infrastructure). It receives the original
  document so that elements the domain does not model (notes, context groups,
  comments) survive without the domain knowing they exist; see D10.
- `SessionRepository` — holds the current `OpenDocument` between reruns.
  Implemented by `SessionStateSessionRepository` (presentation, over
  `st.session_state`). No filesystem implementation exists: export is a browser
  download.

### D4 — Tell-don't-ask against a UI that must read

Object Calisthenics forbids getters, but the screen must render every source.
A domain object is told to describe itself into an application-layer builder,
which yields an immutable `UnitView` / `SessionView` the presentation renders.
Domain exposes no accessors; presentation never holds a domain object.

Alternative considered: read-only properties. Rejected as a direct violation of
a stated project rule.

### D5 — Literal braces are escaped, not forbidden

Masking doubles a literal `{` or `}`; unmasking halves it. A fixture unit
carries literal braces so the path is exercised. Braces inside a placeholder's
attributes (Angular's `INTERPOLATION` `equiv-text="{{ ... }}"`) are not text and
are never escaped.

### D6 — Errors are answers, not exceptions

`CatalogRefusal` and `PlaceholderComparison` are value objects the use cases
return. Nothing in the business layers raises for expected outcomes.

### D7 — Whitespace is escaped before it is marked

The red underline needs `unsafe_allow_html`. Order is fixed: HTML-escape the
content, then wrap leading and trailing whitespace runs in a marked span. A
presentation test asserts a source containing `<p>` renders as visible text.

### D8 — Widget identity is the unit identifier

Every input is keyed by `UnitIdentifier`, never by position, so unit 8 cannot
inherit unit 7's text.

### D9 — Starting over is gated on export being requested

`st.download_button` reports a click, not a completed save. "Upload another
file" therefore appears after a final export is *requested*. Accepted as a
known imprecision.

### D10 — Write by modifying the parsed original, not by rebuilding

`ElementTreeCatalogWriter` re-parses the original document, then for each unit:
leaves an unedited target alone, replaces or inserts the target element of an
edited unit immediately after its `<source>` (copying the source's `tail` so
indentation stays consistent), or removes it when the unit became
untranslated. It sets `target-language` on `<file>` and serialises.
Comments are kept by parsing with `TreeBuilder(insert_comments=True)`; the
XLIFF 1.2 namespace is registered as the default so no `ns0:` prefix appears.
An edited unit is one whose session target differs from the target parsed from
the upload; auto-filled units count as edited.

Alternatives considered: byte-level splicing using expat offsets (exact bytes,
but more machinery; dropped with the byte-equivalence goal); rebuilding the
document from the domain catalog (would lose notes and context groups unless
the domain modelled them).

### D11 — Placeholders carry their name and attributes in order

`Placeholder` holds a `PlaceholderName` and ordered `PlaceholderAttributes`, so
unmasking rebuilds an `<x/>` element with the same `id`, `ctype`, `equiv-text`
and any other attribute, in the original order.

### D12 — Size and encoding are checked before parsing

`OpenCatalog` measures `DocumentSize` against 4 MiB (4,194,304 bytes) and
refuses before the reader runs. The reader then refuses an XML declaration
naming an encoding other than UTF-8 and bytes that do not decode as UTF-8.
`.streamlit/config.toml` sets `server.maxUploadSize = 4` as a first line, but
the domain check is authoritative, since it is testable without Streamlit.
A UTF-8 byte order mark is accepted for now (N4).

### D13 — Unit state and the whitespace rules

```
source is whitespace-only            --> translated, auto-filled (target = source)
target empty or whitespace-only      --> untranslated
target has text, tokens differ       --> invalid
otherwise                            --> translated
```

Auto-filled units are reported on open (`AutoFillReport`), and `UnitView`
carries an auto-filled mark the screen shows as a warning. Clearing an
auto-filled target restores it, so such a unit is never untranslated. A
fresh catalog is one whose units with non-whitespace sources are all
untranslated, so auto-fill never turns a fresh catalog partial.

### D14 — Synthetic fixtures for a CT-scan analysis app

Three hand-written catalogs under `tests/fixtures/`, 60 units each, same unit
identifiers and order, every unit carrying a `<context-group purpose="location">`
and about 20 carrying description or meaning `<note>`s, plus one XML comment:

| Fixture | Role | Profile |
| --- | --- | --- |
| `messages.xlf` | fresh, `source-language="es"`, no target language | 8 units with placeholders (one with 10; one repeating a placeholder id; one `INTERPOLATION`; one button wrapping a `mat-icon`; units 44 and 52 among them); 6 with leading or trailing whitespace, 2 of them non-breaking; 3 with escaped HTML, one over 800 characters; 1 with literal braces; whitespace-only source at unit 30 |
| `messages.en-GB.xlf` | partial, `target-language="en-GB"` | targets for every unit except 30 and 31; unit 38 target whitespace-only; units 44 and 52 lost every placeholder; 4 targets identical to their source; 1 target with `state="translated"` |
| `messages.fr.xlf` | completed, `target-language="fr"` | valid targets for every unit except 30 |

Expected behaviour: fresh opens asking for a language and reports 30 as
auto-filled; en-GB resumes at 31 and refuses a final export naming 31, 38, 44
and 52; fr opens on the download screen.

## Deferred notes

Each is to be carried into `design-notes.md` by the documentation task.

- **N1 — Whitespace-only sources.** Auto-filled as translated, with a warning.
  Revisit whether they should be hidden, excluded from counts, or require an
  explicit acknowledgement.
- **N2 — Work lost on browser refresh.** The session lives in
  `st.session_state`; a reload loses unsaved targets. Not yet specified:
  auto-save, a leave-page warning, or a periodic draft reminder.
- **N3 — Language form.** The translator chooses the target language in a form;
  its control (free text, list, searchable list) and its validation rules are
  not yet specified. `LanguageCode` accepts BCP 47-shaped tags meanwhile.
- **N4 — UTF-8 byte order mark.** Accepted on input for now; whether output
  should keep, drop or refuse it is not yet specified.
- Signature embedding and machine translation remain deferred.

## Risks / Trade-offs

- **A mask/unmask defect corrupts every exported file** → round-trip test over
  every fixture unit, written before any UI code.
- **ElementTree drops something the writer did not touch** → fidelity test
  comparing every non-target element, attribute, text and comment of each
  fixture before and after a write.
- **Escaping order bug renders sources as live HTML** → explicit test per D7.
- **Double dispatch adds indirection** → confined to one builder per view.
- **The two-instance-variable limit strains `TranslationSession` and
  `OpenDocument`** → composition (`CatalogPosition`, `LanguagePair`) rather than
  relaxing the rule.

## Open Questions

- A source repeating one placeholder id (e.g. two `START_BOLD_TEXT`) masks as
  distinct tokens; swapping them yields identical output. Treated as harmless.
- Whether `<note>` descriptions and meanings should be shown to the translator.
  They are preserved, not displayed, in this change.
