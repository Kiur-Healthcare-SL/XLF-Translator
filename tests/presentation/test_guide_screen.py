from support.app_driver import button, go_to, position, started, translating


def guide_text(app):
    return " ".join(markdown.value for markdown in app.markdown)


def test_the_guide_explains_tokens_the_gate_and_drafts():
    app = button(started(), "How it works").click().run()
    text = guide_text(app)
    assert "numbered token" in text
    assert "cannot leave" in text
    assert "Save draft" in text and "resume" in text


def test_the_session_survives_a_visit_to_the_guide():
    app = go_to(translating("messages.xlf"), 7)
    app.text_area[0].input("Reports").run()
    button(app, "How it works").click().run()
    assert app.text_area == []
    button(app, "Back").click().run()
    assert position(app) == "Item 7 of 60"
    assert app.text_area[0].value == "Reports"
