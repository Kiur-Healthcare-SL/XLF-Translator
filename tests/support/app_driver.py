"""Drives the real Streamlit app headlessly with AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest
from support.fixture_documents import FIXTURES

APP = Path(__file__).parents[2] / "src" / "xlf_translator" / "presentation" / "app.py"


def started():
    app = AppTest.from_file(str(APP), default_timeout=30)
    return app.run()


def uploaded(name, content=None):
    app = started()
    return app.file_uploader[0].upload(name, content or (FIXTURES / name).read_bytes()).run()


def translating(name, language="en-GB"):
    app = uploaded(name)
    if app.text_input:
        app.text_input[0].input(language)
        app.button[0].click().run()
    return app


def button(app, label):
    return next(each for each in app.button if each.label == label)


def texts(elements):
    return [element.value for element in elements]


def position(app):
    return next(caption for caption in texts(app.caption) if caption.startswith("Item "))


def go_to(app, ordinal):
    app.number_input(key="go-to-ordinal").set_value(ordinal)
    return button(app, "Go").click().run()
