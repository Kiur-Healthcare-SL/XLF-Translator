# Design

## Context

Greenfield project; no code exists. See proposal.md for motivation.

Two real catalogs constrain every decision and serve as fixtures:
`messages.xlf` (360 units, source language `es`, no targets) and
`messages.en-GB.xlf` (359 targets, two of them with every placeholder deleted,
one unit untranslated whose source is whitespace only). Measured properties of
that data: 28 units carry inline placeholders, 73 placeholder elements in total,
at most 10 in one unit; 42 units carry leading or trailing whitespace, some of
it non-breaking; several sources carry escaped HTML as literal text, the longest
974 characters; **no source or target contains a brace character**; 18 targets
are identical to their source.

The architectural and style constraints are fixed by the project configuration
and are treated here as given, not re-argued.

## Goals / Non-Goals

**Goals:**
- Make placeholder loss impossible to export, whether typed or imported.
- Keep every business rule testable without importing Streamlit.
- Preserve byte-level fidelity of everything the translator does not edit.

**Non-Goals:**
- Machine translation and signature embedding (deferred; see `design-notes.md`).
- XLIFF 2.x, multi-`<file>` documents, and ICU plural or select messages. The
  absence of braces in both catalogs is evidence no ICU messages exist here.
- Concurrent or multi-user editing. One browser session, one catalog.

## Decisions

### D1 — Masking is a domain rule, not a display trick

`{n}` tokens never reach disk; they exist only between parse and serialise.
Because the safety argument rests on them, masking lives in **domain**, not in
presentation or infrastructure, and is exercised by a property test over the
real 360-unit catalog before any UI exists.

Alternative considered: let the translator edit raw `<x .../>` XML. Rejected —
a malformed fragment cannot be parsed, so the app could not name which
placeholder was lost, only that the text no longer parses.

### D2 — Layer assignment

| Concept | Layer |
| --- | --- |
| `TranslationUnit`, `UnitIdentifier`, `SourceContent`, `TargetContent` | domain |
| `Placeholder`, `PlaceholderToken`, `MaskedContent`, `PlaceholderComparison` | domain |
| `Catalog` (first-class collection of units), `CatalogPosition` | domain |
| `LanguageCode`, `ArtifactName` | domain |
| `TranslationSession` (position, catalog, target language) | domain |
| `OpenCatalog`, `MoveToUnit`, `EnterTarget`, `CopySourceIntoTarget`, `ExportDraft`, `ExportFinal` | application |
| `CatalogReader`, `CatalogWriter`, `SessionRepository` (ports) | application |
| `ElementTreeCatalogReader`, `ElementTreeCatalogWriter` | infrastructure |
| `SessionStateSessionRepository` | presentation (implements an application port) |
| Screens, widgets, whitespace markup, download buttons | presentation |

### D3 — Ports and their implementations

- `CatalogReader` — takes uploaded bytes, answers a `Catalog` or a
  `CatalogRefusal`. Implemented by `ElementTreeCatalogReader` (infrastructure,
  `xml.etree.ElementTree`).
- `CatalogWriter` — takes a `Catalog` and a `LanguageCode`, answers document
  bytes. Implemented by `ElementTreeCatalogWriter` (infrastructure).
- `SessionRepository` — holds the current `TranslationSession` between reruns.
  Implemented by `SessionStateSessionRepository` (presentation, over
  `st.session_state`). The port is declared in application; the only
  implementation is a presentation adapter because Streamlit owns the lifetime.
  No filesystem implementation exists: export is a browser download, so
  infrastructure never writes a file.

### D4 — Tell-don't-ask against a UI that must read

Object Calisthenics forbids getters, but the screen must render 360 sources.
Resolved by double dispatch: a domain object is told to describe itself into an
application-layer builder, which yields an immutable `UnitView` / `SessionView`
the presentation renders. Domain exposes no accessors; presentation never holds
a domain object.

Alternative considered: pragmatic read-only properties on entities. Rejected as
a direct violation of a stated project rule.

### D5 — Literal braces are escaped, not forbidden

Masking doubles a literal `{` or `}`; unmasking halves it. Neither catalog
contains one today, so the path is rare, but a future catalog must not silently
corrupt. Alternative considered: refusing such files, which would make the app
fail on valid input.

### D6 — Errors are answers, not exceptions

`CatalogRefusal` and `PlaceholderComparison` are value objects the use cases
return. Presentation renders them; nothing in the business layers raises for
expected outcomes. Keeps the navigation gate free of try/except and testable as
a pure function of unit state.

### D7 — Whitespace is escaped before it is marked

The red underline needs `unsafe_allow_html`. Sources containing literal
`<p>`/`<ul>` text would otherwise render as real markup. Order is fixed:
HTML-escape the content, then wrap leading and trailing whitespace runs in a
marked span. A presentation-layer unit test asserts that a source containing
`<p>` renders as visible text.

### D8 — Widget identity is the unit identifier

Every input is keyed by `UnitIdentifier`, never by position. Keying by position
makes unit 8 inherit unit 7's text — the classic Streamlit defect, and with 360
units it would be hit immediately.

### D9 — Starting over is gated on export being requested

`st.download_button` reports a click, not a completed save; a cancelled OS save
dialog is indistinguishable from a successful one. "Upload another file"
therefore appears after a final export is *requested*. Accepted as a known
imprecision rather than adding a manual "I saved it" confirmation.

## Risks / Trade-offs

- **A mask/unmask defect corrupts every exported file** → property test
  `unmask(mask(source)) == source` over all 360 real units, plus both catalogs
  as committed fixtures, written before any UI code.
- **Escaping order bug renders sources as live HTML** → explicit test per D7.
- **Double dispatch adds indirection for every rendered field** → confined to
  one builder per view; the alternative breaks a project rule.
- **The navigation gate can feel obstructive on a long unit** → clearing the
  target is always permitted, so a translator is never without a legal move.
- **The two-instance-variable limit will strain `TranslationSession`**, which
  naturally wants catalog, position and target language → composition
  (`CatalogPosition` holding position within a catalog) rather than relaxing the
  rule.

## Open Questions

These are recorded as assumptions in proposal.md and written into the specs; if
any is answered differently, the named spec changes.

- Emitting corrected `source-language`/`target-language` makes output diverge
  from the repo's current convention (`xliff-catalog`).
- Auto-filling whitespace-only sources (`xliff-catalog`); the alternative is
  excluding them from the completeness count.
- Whether a final export should also refuse untranslated units, or whether
  completion already makes that unreachable (`file-exchange`).
