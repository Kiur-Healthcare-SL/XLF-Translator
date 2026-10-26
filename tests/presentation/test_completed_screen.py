from support.app_driver import button, position, texts, translating, uploaded


def labels(app):
    return [each.label for each in app.button]


def finish(app):
    return button(app, "Finish").click().run()


def test_a_completed_catalog_opens_on_the_download_screen():
    app = uploaded("messages.fr.xlf")
    assert any("messages.fr.xlf" in message for message in texts(app.success))
    assert [download.label for download in app.download_button] == ["Download", "Save draft"]


def test_an_incomplete_catalog_lists_every_unresolved_item():
    app = finish(translating("messages.en-GB.xlf"))
    assert "Download" not in [download.label for download in app.download_button]
    unresolved = [label for label in labels(app) if label.startswith("Go to item")]
    assert unresolved == [
        "Go to item 31 (untranslated)",
        "Go to item 38 (untranslated)",
        "Go to item 44 (tokens do not match)",
        "Go to item 52 (tokens do not match)",
    ]


def test_each_listed_item_jumps_to_its_unit():
    app = finish(translating("messages.en-GB.xlf"))
    button(app, "Go to item 52 (tokens do not match)").click().run()
    assert position(app) == "Item 52 of 60"


def test_upload_another_file_appears_only_after_a_final_export_is_requested():
    app = uploaded("messages.fr.xlf")
    assert "Upload another file" not in labels(app)
    app.download_button[0].click().run()
    assert "Upload another file" in labels(app)


def test_upload_another_file_returns_to_an_empty_upload_screen():
    app = uploaded("messages.fr.xlf")
    app.download_button[0].click().run()
    button(app, "Upload another file").click().run()
    assert texts(app.title) == ["XLF Translator"]
    assert app.file_uploader[0].value is None
