from support.app_driver import position, texts, translating, uploaded


def test_a_fresh_catalog_asks_for_a_target_language():
    app = uploaded("messages.xlf")
    assert len(app.text_input) == 1
    assert app.text_area == []


def test_the_chosen_language_reaches_the_session():
    app = translating("messages.xlf", "en-GB")
    assert position(app) == "Item 1 of 60"
    assert app.session_state["xlf_translator.open_document"].describe().target_language == "en-GB"


def test_a_malformed_language_is_refused():
    app = uploaded("messages.xlf")
    app.text_input[0].input("English")
    app.button[0].click().run()
    assert "language code" in app.error[0].value
    assert len(app.text_input) == 1


def test_the_form_is_skipped_when_the_document_declares_a_language():
    app = uploaded("messages.en-GB.xlf")
    assert app.text_input == []
    assert texts(app.title) == ["messages.en-GB.xlf"]
