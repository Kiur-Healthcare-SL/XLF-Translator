# Design notes

Decisions deliberately left open by the `xlf-translator-app` change, and work
deferred to later changes. Each note records what the application does today
and what remains to be decided.

## N1 — Whitespace-only sources

A unit whose source holds only whitespace is auto-filled as translated, with its
target set to its source, and the translator is warned which units were
auto-filled. Still to decide: whether such units should be hidden, excluded
from counts, or require an explicit acknowledgement.

## N2 — Work lost on browser refresh

The translation session lives in Streamlit's session state, so reloading the
page loses every target not yet saved as a draft. Still to decide: auto-save, a
leave-page warning, or a periodic reminder to save a draft.

## N3 — Language form

A catalog that declares no target language asks the translator to choose one in
a form. Its control (free text, list, searchable list) and its validation rules
are not specified; meanwhile any BCP 47-shaped tag is accepted.

## N4 — UTF-8 byte order mark

A UTF-8 byte order mark is accepted on input. Whether output should keep, drop
or refuse it is not specified.

## Deferred work

- **Signature embedding.** Signing a finished catalog or embedding a signature
  image was part of the original idea and is out of scope for now.
- **Machine translation.** Suggesting translations automatically is out of
  scope for now; the translator may copy the source into the target as a
  starting point instead.
