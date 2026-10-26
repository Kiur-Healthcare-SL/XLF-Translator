# Proposal

## Why

Angular i18n catalogs are translated by hand in a text editor, and the cost is
visible in a shipped `ace-app` catalog: two units lost all their `<x/>`
placeholders, so a dialog's close button no longer renders. A guided tool that
makes placeholder loss impossible to export removes that class of bug.

## What Changes

- New Streamlit app: upload an `.xlf`, translate one unit per screen, download.
- Parse XLIFF 1.2 encoded as UTF-8, up to 4 MiB. Refuse anything else, and
  any document declaring no source language, naming what was expected.
- Mask inline `<x/>` placeholders as `{1}`...`{n}` while editing; unmask
  losslessly on write.
- Refuse navigation off a unit whose target placeholders differ from its
  source's. Clearing the target is always permitted.
- Classify uploads by content: fresh, partial, completed. Resume at the first
  unresolved unit.
- A fresh catalog declares no target language: the translator chooses one in a
  language form. A re-uploaded draft declares one, and it is adopted.
- Whitespace-only sources are auto-filled as translated, and the translator is
  warned which units were auto-filled. A whitespace-only target counts as
  untranslated.
- "Save draft" is always permitted and names its file
  `<stem>.<target-language>.draft.xlf`. "Download" is refused while any unit is
  untranslated or invalid and names its file `<stem>.<target-language>.xlf`.
  Both go through the browser save dialog and declare both languages.
- Output keeps every element the app does not edit, including `<note>` and
  `<context-group>`. Byte-level formatting is not guaranteed.
- A docs screen describing the intended workflow.
- Synthetic test fixtures for an imaginary CT-scan (TAC) analysis app, modelled
  on the measured profile of the `ace-app` catalogs but not copied from them.
- `AGENTS.md` updated to the current product; `design-notes.md` created to hold
  deferred decisions.
- Non-goals: machine translation, signature embedding, encodings other than
  UTF-8.

## Capabilities

### New Capabilities
- `xliff-catalog`: parsing, refusal, classification and serialisation of XLIFF
  1.2, including language metadata and preservation of unedited elements.
- `placeholder-masking`: the bijection between `<x/>` elements and `{n}` tokens,
  and placeholder equality between source and target.
- `translation-session`: unit state, navigation, the navigation gate, resume
  position, auto-fill warnings and completion.
- `file-exchange`: upload limits, target language, artifact naming, export
  gates.
- `app-guide`: the documentation screen and how it is reached.

### Modified Capabilities
None. The project has no existing specs.

## Impact

A new standalone Python project: Streamlit, stdlib ElementTree, pytest, four
layers. `ace-app` is unmodified and is not a dependency; its catalogs informed
the fixture profile only. `AGENTS.md` and `openspec/config.yaml` are aligned
with the revised product.

## Deferred

Recorded in design.md, later in `design-notes.md`: whitespace-only auto-fill
(N1), work lost on refresh (N2), language form controls (N3), byte order marks
(N4).

## Risks

- A mask/unmask defect corrupts every file written. Mitigated by a round-trip
  test over every fixture unit, before any UI.
- Marking whitespace needs `unsafe_allow_html`, which renders literal `<p>` text
  in sources unless escaped first.
- Streamlit widget state keyed by anything but unit id leaks targets between
  units.
