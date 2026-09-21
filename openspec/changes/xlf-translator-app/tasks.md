# Tasks

Every task that adds a class adds its dedicated unit test file mirroring the
package path. Tasks are sized at one hour or less.

## 1. Scaffolding and guards

- [ ] 1.1 Create the four-layer package structure and a mirrored `tests/` tree; verify `pytest` runs and reports zero tests without error
- [ ] 1.2 Add `pyproject.toml` with Streamlit and pytest; verify a clean install succeeds and `streamlit --version` runs
- [ ] 1.3 Commit `messages.xlf` and `messages.en-GB.xlf` as fixtures; verify a test asserts 360 units in each and 359 targets in the second
- [ ] 1.4 Add an import-direction guard test asserting domain imports no Streamlit, no XML library and no outer layer; verify it fails when a deliberate violating import is added
- [ ] 1.5 Add an AST-based limits test for functions under 20 lines, classes under 200 lines and one class per file; verify it reports a deliberately oversized sample

## 2. Domain: identity and language

- [ ] 2.1 Add `UnitIdentifier` and its test; verify equality, rejection of an empty identifier, and use as a dictionary key
- [ ] 2.2 Add `LanguageCode` and its test; verify acceptance of `es` and `en-GB` and rejection of malformed tags
- [ ] 2.3 Add `ArtifactName` and its test; verify it renders `messages.en-GB.draft.xlf` and `messages.en-GB.xlf` from a stem and a language

## 3. Domain: content and placeholders

- [ ] 3.1 Add `PlaceholderName` and `PlaceholderAttributes` with their tests; verify attribute round-tripping for content type and equivalent text
- [ ] 3.2 Add `Placeholder` and its test; verify two placeholders with the same name and attributes are equal and that it reports the markup it stands for
- [ ] 3.3 Add `PlaceholderToken` and its test; verify rendering as `{1}` and parsing of `{10}`, and rejection of `{0}` and `{1`
- [ ] 3.4 Add `Content` as a first-class collection of text runs and placeholders with its test; verify text-only content, placeholder-only content, and content whose text contains `<p>` as literal characters

## 4. Domain: masking

- [ ] 4.1 Add `ContentMask` and its test; verify a paired-placeholder source masks to `{1}limited functionality{2}` and placeholder-free content is unchanged
- [ ] 4.2 Add `ContentUnmask` and its test; verify tokens restore placeholder name, content type and equivalent text, and that `{2}word{1}` restores in reversed order
- [ ] 4.3 Add literal-brace escaping to both and extend their tests; verify content containing a literal `{1}` round-trips and yields no token
- [ ] 4.4 Add the round-trip property test over every unit of both fixtures; verify `unmask(mask(source)) == source` holds for all 360 units in each catalog
- [ ] 4.5 Add `PlaceholderComparison` and its test; verify it names a missing token with its markup, a repeated token, and an unknown token, and passes on reordered tokens

## 5. Domain: units, catalog, session

- [ ] 5.1 Add `TranslationUnit` and its test; verify the three states, that a target equal to its source is translated, and that a whitespace-only source is translated on construction
- [ ] 5.2 Add `Catalog` as a first-class collection with its test; verify document order, ordinal lookup, and rejection of duplicate identifiers
- [ ] 5.3 Add catalog classification with its test; verify fresh, partial and completed against both fixtures
- [ ] 5.4 Add `CatalogPosition` and its test; verify absolute position reporting, refusal to step past either end, and jump to an ordinal
- [ ] 5.5 Add `TranslationSession` and its test; verify resume lands on ordinal 66 for `messages.en-GB.xlf`
- [ ] 5.6 Add the navigation gate to `TranslationSession` and extend its test; verify both directions are refused while the current unit is invalid and permitted once the target is cleared
- [ ] 5.7 Add completion reporting with its test; verify it names the ordinals of all unresolved units

## 6. Application: views, ports, use cases

- [ ] 6.1 Add `UnitView` and `SessionView` builders with their tests; verify a unit describes itself without the domain exposing accessors
- [ ] 6.2 Declare the `CatalogReader`, `CatalogWriter` and `SessionRepository` ports with in-memory fakes and their tests; verify the fakes satisfy the ports
- [ ] 6.3 Add `OpenCatalog` and its test; verify a fresh catalog requires a target language and a catalog declaring `en-GB` adopts it without asking
- [ ] 6.4 Add `MoveToUnit` and its test; verify stepwise movement, jumping, and refusal while the current unit is invalid
- [ ] 6.5 Add `EnterTarget` and its test; verify state transitions and that the placeholder difference is returned on mismatch
- [ ] 6.6 Add `CopySourceIntoTarget` and its test; verify tokens, leading non-breaking spaces and escaped markup all arrive in the target
- [ ] 6.7 Add `ExportDraft` and its test; verify it succeeds while a unit is invalid and names the artifact `messages.en-GB.draft.xlf`
- [ ] 6.8 Add `ExportFinal` and its test; verify refusal listing unresolved ordinals and success naming `messages.en-GB.xlf`

## 7. Infrastructure: XLIFF

- [ ] 7.1 Add `ElementTreeCatalogReader` and its test; verify 360 units parse from the fixture with whitespace and inline placeholders intact
- [ ] 7.2 Add `CatalogRefusal` answers to the reader and extend its test; verify refusal of non-XML, of version 2.0, of a document with no units, and of duplicate identifiers, each naming expectation and finding
- [ ] 7.3 Add `ElementTreeCatalogWriter` and its test; verify no `state` attribute, no target element for untranslated units, and both language attributes declared
- [ ] 7.4 Add a serialisation round-trip test across both fixtures; verify re-parsing the output yields an equal catalog

## 8. Presentation

- [ ] 8.1 Add `SessionStateSessionRepository` and its test; verify a session survives a simulated rerun and is keyed independently of widget state
- [ ] 8.2 Build the upload screen; verify a valid catalog opens a session and a refused document leaves none, showing the reason
- [ ] 8.3 Build target-language selection for fresh catalogs; verify the chosen code reaches the session and is skipped when the document declares one
- [ ] 8.4 Build the translation screen layout with the file name as heading, source left, target right, and "item x of 360" above the target; verify against a session fixture
- [ ] 8.5 Add the whitespace marker renderer and its test; verify a source containing `<p>` renders as visible text and leading whitespace is marked
- [ ] 8.6 Wire Prev, Next and the copy button, each keyed by unit identifier; verify unit 8 does not inherit unit 7's text
- [ ] 8.7 Wire the navigation gate into the screen; verify the refusal message names the missing token and both buttons are inert while invalid
- [ ] 8.8 Add the go-to-ordinal control; verify it moves within range and refuses an ordinal outside the catalog
- [ ] 8.9 Add the "Save draft" download; verify it is offered while a unit is invalid and delivers the draft-named artifact
- [ ] 8.10 Build the completed screen with the gated final download and the unresolved list; verify each listed ordinal jumps to its unit
- [ ] 8.11 Gate "Upload another file" on a requested final export; verify it is absent before and present after
- [ ] 8.12 Build the docs screen and its entry point; verify the session position and entered targets survive a visit

## 9. Acceptance

- [ ] 9.1 Add an end-to-end test over `messages.en-GB.xlf`; verify it classifies as partial, resumes at ordinal 66, and refuses the final export while naming the two units whose placeholders were deleted
- [ ] 9.2 Add an end-to-end test over `messages.xlf`; verify a fresh catalog requires a target language, accepts a translation, and exports a draft that re-opens as partial
- [ ] 9.3 Run the app manually end to end against both fixtures; verify the screens, gates and downloads behave as the specs describe
