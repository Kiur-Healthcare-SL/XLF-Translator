# Tasks

Every task that adds a class adds its dedicated unit test file mirroring the
package path. Tasks are sized at one hour or less.

## 1. Scaffolding, fixtures and project documents

- [x] 1.1 Create the four-layer package structure and a mirrored `tests/` tree; verify `pytest` runs and reports zero tests without error
- [x] 1.2 Add `pyproject.toml` with Streamlit and pytest, and `.streamlit/config.toml` setting `server.maxUploadSize = 4`; verify a clean install succeeds and `streamlit --version` runs
- [x] 1.3 Write `tests/fixtures/messages.xlf`, a fresh 60-unit Spanish catalog for a CT-scan (TAC) analysis app following the profile in design D14, with context groups, notes and one comment; verify it is well-formed and declares `source-language="es"` and no target language
- [x] 1.4 Write `tests/fixtures/messages.en-GB.xlf` from the same units following D14 (no targets at 30 and 31, whitespace-only target at 38, placeholders deleted at 44 and 52); verify it is well-formed and declares `target-language="en-GB"`
- [x] 1.5 Write `tests/fixtures/messages.fr.xlf`, a completed French catalog of the same units; verify it is well-formed and every unit except 30 carries a target
- [x] 1.6 Add a fixture profile test using only the standard library; verify unit counts, shared identifiers, the placeholder, whitespace, escaped-HTML, brace, note and context-group counts of D14, and that every file is under 4 MiB
- [x] 1.7 Add an import-direction guard test asserting domain imports no Streamlit, no XML library and no outer layer; verify it fails when a deliberate violating import is added
- [x] 1.8 Add an AST-based limits test for functions under 20 lines, classes under 200 lines and one class per file; verify it reports a deliberately oversized sample
- [x] 1.9 Update `AGENTS.md`: describe the product as one unit per screen with drafts and no signing, drop file I/O and compression from the infrastructure row, and point to `design-notes.md`; verify no reference to pagination, batches or signing remains
- [x] 1.10 Create `design-notes.md` holding deferred notes N1 to N4 and the deferred signature and machine-translation work, and align the `openspec/config.yaml` context (structural fidelity instead of byte equivalence, size and encoding limits); verify every link to `design-notes.md` resolves

## 2. Domain: identity, language and documents

- [x] 2.1 Add `UnitIdentifier` and its test; verify equality, rejection of an empty identifier, and use as a dictionary key
- [x] 2.2 Add `LanguageCode` and its test; verify acceptance of `es`, `fr` and `en-GB` and rejection of malformed tags
- [x] 2.3 Add `LanguagePair` and its test; verify a pair with a source and no target, and adoption of a target
- [x] 2.4 Add `ArtifactName` and its test; verify it renders `messages.en-GB.draft.xlf` and `messages.en-GB.xlf` from a stem and a language
- [x] 2.5 Add `DocumentSize` and its test; verify 4,194,304 bytes is within the limit and 4,194,305 is not
- [x] 2.6 Add `UploadedDocument` and `CatalogRefusal` with their tests; verify the stem is taken from `messages.xlf` and a refusal states expectation and finding

## 3. Domain: content and placeholders

- [x] 3.1 Add `PlaceholderName` and `PlaceholderAttributes` with their tests; verify attributes keep their order and round-trip content type and equivalent text
- [x] 3.2 Add `Placeholder` and its test; verify two placeholders with the same name and attributes are equal and that it reports the markup it stands for
- [x] 3.3 Add `PlaceholderToken` and its test; verify rendering as `{1}` and parsing of `{10}`, and rejection of `{0}` and `{1`
- [x] 3.4 Add `Content` as a first-class collection of text runs and placeholders with its test; verify text-only content, placeholder-only content, content whose text contains `<p>` as literal characters, and whitespace-only detection

## 4. Domain: masking

- [x] 4.1 Add `ContentMask` and its test; verify a paired-placeholder source masks to `{1}limited functionality{2}` and placeholder-free content is unchanged
- [x] 4.2 Add `ContentUnmask` and its test; verify tokens restore placeholder name and attributes in order, and that `{2}word{1}` restores in reversed order
- [x] 4.3 Add literal-brace escaping to both and extend their tests; verify content containing a literal `{1}` round-trips and yields no token
- [x] 4.4 Add `PlaceholderComparison` and its test; verify it names a missing token with its markup, a repeated token, and an unknown token, and passes on reordered tokens

## 5. Domain: units, catalog, session

- [x] 5.1 Add `TranslationUnit` and its test; verify the three states, that empty and whitespace-only targets are untranslated, and that a target equal to its source is translated
- [x] 5.2 Add whitespace-only source auto-fill to `TranslationUnit` and extend its test; verify such a unit is translated and auto-filled, and that clearing its target restores the source
- [x] 5.3 Add `Catalog` as a first-class collection with its test; verify document order, ordinal lookup, and rejection of duplicate identifiers
- [x] 5.4 Add `CatalogClassification` and its test; verify fresh (including a catalog with one auto-filled unit), partial (a gap, or imported damage) and completed
- [x] 5.5 Add `CatalogPosition` and its test; verify absolute position reporting, refusal to step past either end, and jump to an ordinal
- [x] 5.6 Add `TranslationSession` and its test; verify resume lands on the first untranslated or invalid unit, passing over auto-filled units
- [x] 5.7 Add the navigation gate to `TranslationSession` and extend its test; verify both directions are refused while the current unit is invalid and permitted once the target is cleared
- [x] 5.8 Add `CompletionReport` and `AutoFillReport` with their tests; verify completion names untranslated and invalid ordinals together, and auto-fill names ordinal 30

## 6. Application: views, ports, use cases

- [x] 6.1 Add `UnitView` and `SessionView` builders with their tests; verify a unit describes itself, including its auto-filled mark, without the domain exposing accessors
- [x] 6.2 Declare the `CatalogReader`, `CatalogWriter` and `SessionRepository` ports with in-memory fakes and their tests; verify the fakes satisfy the ports and the writer receives the original document
- [x] 6.3 Add `OpenDocument` and `OpenCatalog` with their tests; verify an oversized document is refused before the reader is called, and that opening reports auto-filled ordinals
- [x] 6.4 Add `ChooseTargetLanguage` and extend `OpenCatalog`'s test; verify a fresh catalog requires a language and a catalog declaring `en-GB` adopts it without asking
- [x] 6.5 Add `MoveToUnit` and its test; verify stepwise movement, jumping, and refusal while the current unit is invalid
- [x] 6.6 Add `EnterTarget` and its test; verify state transitions, that a whitespace-only target is untranslated, and that the placeholder difference is returned on mismatch
- [x] 6.7 Add `CopySourceIntoTarget` and its test; verify tokens, leading non-breaking spaces and escaped markup all arrive in the target
- [x] 6.8 Add `ExportDraft` and its test; verify it succeeds while units are untranslated or invalid and names the artifact `messages.en-GB.draft.xlf`
- [x] 6.9 Add `ExportFinal` and its test; verify refusal naming untranslated and invalid ordinals, and success naming `messages.en-GB.xlf`

## 7. Infrastructure: XLIFF

- [x] 7.1 Add `ElementTreeCatalogReader` and its test; verify the fresh fixture parses to 60 units with whitespace, inline placeholders and source language `es` intact
- [x] 7.2 Extend the reader to read existing targets and the declared target language; verify the en-GB fixture yields targets for 58 units and target language `en-GB`
- [x] 7.3 Add refusals to the reader and extend its test; verify refusal of non-XML, a non-UTF-8 declaration, invalid UTF-8 bytes, version 2.0, no file element, no source language, no units and duplicate identifiers, each naming expectation and finding
- [x] 7.4 Add `ElementTreeCatalogWriter` and its test; verify a new target follows its source with no `state`, an edited imported target is replaced, a cleared target is removed, and `target-language` is declared
- [x] 7.5 Add the fidelity test over all three fixtures; verify notes, context groups, comments, untouched targets with their `state`, and the default namespace survive a write with no `ns0:` prefix
- [x] 7.6 Add the round-trip tests across all three fixtures; verify `unmask(mask(content))` equals the original for every source and target, and re-parsing writer output yields an equal catalog

## 8. Presentation

- [x] 8.1 Add `SessionStateSessionRepository` and its test; verify an open document survives a simulated rerun and is keyed independently of widget state
- [x] 8.2 Build the upload screen; verify a valid catalog opens a session and a refused document (too large, wrong encoding, no source language) leaves none, showing the reason
- [x] 8.3 Build the language form for fresh catalogs; verify the chosen code reaches the session and the form is skipped when the document declares a target language
- [x] 8.4 Build the translation screen layout with the file name as heading, source left, target right, and "item x of 60" above the target; verify against a session fixture
- [x] 8.5 Add the whitespace marker renderer and its test; verify a source containing `<p>` renders as visible text and leading whitespace is marked
- [x] 8.6 Show the auto-fill warnings: a notice on open listing auto-filled ordinals, and a mark on an auto-filled current unit; verify both appear for unit 30 of the fresh fixture
- [x] 8.7 Wire Prev, Next and the copy button, each keyed by unit identifier; verify unit 8 does not inherit unit 7's text
- [x] 8.8 Wire the navigation gate into the screen; verify the refusal message names the missing token and both buttons are inert while invalid
- [x] 8.9 Add the go-to-ordinal control; verify it moves within range and refuses an ordinal outside the catalog
- [x] 8.10 Add the "Save draft" download; verify it is offered while units are untranslated or invalid and delivers the draft-named artifact
- [x] 8.11 Build the completed screen with the gated final download and the unresolved list; verify each listed ordinal jumps to its unit
- [x] 8.12 Gate "Upload another file" on a requested final export; verify it is absent before and present after
- [x] 8.13 Build the docs screen and its entry point; verify the session position and entered targets survive a visit

## 9. Acceptance

- [x] 9.1 Add an end-to-end test over `messages.en-GB.xlf`; verify it classifies as partial, resumes at ordinal 31, and refuses the final export naming 31, 38, 44 and 52
- [x] 9.2 Add an end-to-end test over `messages.xlf`; verify it requires a target language, reports unit 30 as auto-filled, accepts a translation, and exports a draft that re-opens as partial declaring both languages with its notes and context groups intact
- [x] 9.3 Add an end-to-end test over `messages.fr.xlf`; verify it classifies as completed, adopts `fr`, and produces `messages.fr.xlf` as a final export
- [ ] 9.4 Run the app manually end to end against all three fixtures; verify the screens, gates, warnings and downloads behave as the specs describe
