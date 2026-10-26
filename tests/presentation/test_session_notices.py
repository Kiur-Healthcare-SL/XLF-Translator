from support.app_driver import texts, translating


def test_auto_filled_units_are_listed_on_open():
    app = translating("messages.xlf")
    assert any("unit 30" in notice for notice in texts(app.info))


def test_the_draft_download_is_offered():
    app = translating("messages.xlf")
    assert [download.label for download in app.download_button] == ["Save draft"]
