import streamlit as st

from xlf_translator.presentation.screen_state import ScreenState

GUIDE = """
### Uploading a catalog
Upload an Angular XLIFF 1.2 file (`.xlf`), encoded as UTF-8 and at most 4 MiB. A file
that is anything else is refused, and the message says what was expected and what was
found. A catalog with no target language asks for one first; a draft you saved earlier
already names its language and opens where you left off.

### What the numbered tokens are
Angular marks bold text, links, icons, line breaks and interpolations such as
`{{ patient.name }}` with inline placeholders. Each one is shown as a numbered token:
`{1}`, `{2}` and so on. Keep every token of the source in your translation, in whatever
order the sentence needs. The app puts the original markup back when it writes the file.
A brace that is part of the text is shown doubled, `{{`, so it cannot be mistaken for
a token.

### Why you cannot leave some units
If a translation drops, repeats or invents a token, the unit is invalid and Prev, Next,
Go and Finish are refused until the tokens match. The message names each token at fault
and the markup it stands for. Clearing the target always releases the unit, so you can
come back to it later.

### Saving and resuming work
Use **Save draft** at any time. It downloads `<name>.<language>.draft.xlf` with
everything translated so far, even with units unfinished or invalid. Reloading the page
loses unsaved work, so save drafts as you go. Upload the draft later to resume at the
first unit that still needs work.

### Exporting the finished catalog
**Finish** lists any unit still untranslated or invalid, each a click away. Once every
unit is translated, **Download** gives `<name>.<language>.xlf`. Notes, context groups and
comments in the original file are kept.

Units whose source is only whitespace are filled in for you, and you are told which.
"""


def render_guide_screen(screen: ScreenState) -> None:
    st.title("How the translator works")
    st.markdown(GUIDE)
    st.button("Back", on_click=screen.close_guide)
