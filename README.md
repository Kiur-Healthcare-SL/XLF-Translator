# XLF Translator

## Index

- [Summary](#summary)
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [First steps](#first-steps)

## Summary

A Streamlit app for translating Angular XLIFF 1.2 (`.xlf`) message catalogs one
unit at a time. Inline placeholders are shown as `{1}`, `{2}`... tokens, and a
unit whose tokens don't match its source can't be left or exported, so markup
can't be lost. Drafts can be saved at any time and resumed later.

## Overview

| Path | Contents |
| --- | --- |
| `src/` | The application package `xlf_translator`: `domain`, `application`, `infrastructure` and `presentation` layers |
| `tests/` | Pytest suite mirroring `src/`, plus the sample `.xlf` fixtures in `tests/fixtures/` |
| `openspec/` | OpenSpec project config, main specs and archived changes |
| `tools/` | The git write guard used by agent hooks |
| `.streamlit/` | Streamlit settings (4 MiB upload limit) |
| `.claude/`, `.opencode/`, `.agents/` | Agent commands, skills and plugins |
| `claude_sessions/` | Saved agent session transcripts |
| `AGENTS.md` | Working agreement for agents: architecture and code style |
| `design-notes.md` | Deferred decisions and future work |
| `pyproject.toml` | Package metadata and dependencies |

## Requirements

- Python 3.11 or later
- `pip`, or [`uv`](https://docs.astral.sh/uv/)
- A modern web browser

Python dependencies (Streamlit, and pytest for development) are declared in
[pyproject.toml](pyproject.toml).

## Installation

1. Clone the repository and enter it:

   ```bash
   git clone <repository-url>
   cd hello-openspec
   ```

2. Create and activate a virtual environment:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project with its development dependencies:

   ```bash
   pip install -e '.[dev]'
   ```

4. Run the tests (optional):

   ```bash
   pytest
   ```

5. Start the app:

   ```bash
   streamlit run src/xlf_translator/presentation/app.py
   ```

   Streamlit prints a local URL, usually <http://localhost:8501>.

## First steps

1. **Launch.** Run the `streamlit run` command above and open the URL it
   prints.
2. **Upload.** Choose an `.xlf` file (UTF-8, at most 4 MiB). If the file
   declares no target language, enter one, such as `en-GB`. A previously saved
   draft opens at the first unit that still needs work.
3. **Translate.** The source is on the left and the target on the right. Keep
   every `{n}` token from the source; the order can change. **Copy source**
   pastes the source into the target as a starting point. Move with
   **Prev**, **Next** or **Go**. If a unit's tokens don't match, you can't
   leave it until you fix them or clear the target.
4. **Save a draft.** **Save draft** downloads
   `<name>.<language>.draft.xlf` at any time. Upload it later to resume.
5. **Finish.** **Finish** lists any unit that is untranslated or has
   mismatched tokens, each one a click away. When every unit is done,
   **Download** gives `<name>.<language>.xlf`.

**How it works** in the sidebar explains these rules in the app.
