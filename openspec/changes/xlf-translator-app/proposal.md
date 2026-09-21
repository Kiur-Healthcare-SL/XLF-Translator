# Proposal

## Why

Angular i18n catalogs are translated by hand in a text editor, and the cost is
visible in this project's shipped `messages.en-GB.xlf`: two units lost all four
of their `<x/>` placeholders, so a dialog's close button no longer renders in
the en-GB build, and one unit was never translated. A guided tool that makes
placeholder loss structurally impossible removes that class of bug before it
ships.

## What Changes

- New Streamlit app: upload an `.xlf`, translate one unit per screen, download.
- Parse XLIFF 1.2; reject non-conforming files, naming what was expected.
- Mask inline `<x/>` placeholders as `{1}`...`{n}` while editing; unmask
  losslessly on write.
- Refuse navigation off a unit whose target placeholders differ from its
  source's. Clearing the target is always permitted, so no unit traps the
  translator.
- Classify uploads by content, not filename: fresh, partial, completed. Resume
  at the first unresolved unit; a completed file opens on the download screen.
- "Save draft" and "Download" both emit an `.xlf` via the browser save dialog.
  Draft naming: `<stem>.<target-language>.draft.xlf`.
- A docs screen describing the intended workflow.
- **ASSUMPTION** Emit correct `source-language` and `target-language`, and omit
  `state` on `<target>`. The repo's current output carries
  `source-language="en-US"` and no target language.
- Non-goals: machine translation and signature embedding, both deferred and
  retained in `design-notes.md`.

## Capabilities

### New Capabilities
- `xliff-catalog`: parsing, classification and serialisation of XLIFF 1.2,
  including file metadata and `<target>` emission rules.
- `placeholder-masking`: the bijection between `<x/>` elements and `{n}` tokens,
  and placeholder equality between source and target.
- `translation-session`: per-unit state, navigation, the navigation gate, resume
  position and completion.
- `file-exchange`: upload acceptance and rejection, artifact naming, download
  gate.
- `app-guide`: the documentation screen and how it is reached.

### Modified Capabilities
None. The project has no existing specs.

## Impact

A new standalone Python project: Streamlit, stdlib ElementTree, pytest, four
layers. `ace-app` is unmodified; its catalogs are acceptance fixtures.

## Assumptions

- **A1** Uploads may contain invalid targets; those units enter an `invalid`
  state and must be repaired before download.
- **A2** Whitespace-only sources are auto-filled with their own source at parse
  time, so item 66 does not strand a resuming translator.
- **A3** A "go to item N" control exists alongside Prev/Next.
- **A4** Save draft is never gated; only navigation and download are.
- **A5** A target identical to its source is valid; this occurs 18 times in real
  data.

## Open Questions

- Correct metadata, or bit-compatibility with the existing toolchain?
- Whitespace-only units: auto-fill, exclude from the count, or treat normally?
- Must the download gate also refuse untranslated units, or is that unreachable
  by construction?

## Risks

- A mask/unmask defect corrupts every file written. Mitigated by a round-trip
  property test over all 360 real units, before any UI.
- Marking whitespace needs `unsafe_allow_html`, which renders the literal
  `<p>`/`<ul>` text in sources unless escaped first.
- Streamlit widget state keyed by anything but unit id leaks targets between
  units.
