from xlf_translator.presentation.screen_state import FINISH, GUIDE, TRANSLATE, ScreenState


def test_translation_is_shown_by_default():
    assert ScreenState({}).current() == TRANSLATE


def test_the_guide_returns_to_the_screen_it_was_opened_from():
    screen = ScreenState({})
    screen.show(FINISH)
    screen.open_guide()
    assert screen.current() == GUIDE
    screen.close_guide()
    assert screen.current() == FINISH


def test_starting_over_resets_the_uploader_and_the_export_request():
    screen = ScreenState({})
    first_key = screen.upload_key()
    screen.request_final_export()
    assert screen.final_export_requested()
    screen.start_over()
    assert screen.upload_key() != first_key
    assert not screen.final_export_requested()


def test_a_message_is_shown_once():
    screen = ScreenState({})
    screen.tell(("There is no unit 500; choose 1 to 60.",))
    assert screen.take_message() == ("There is no unit 500; choose 1 to 60.",)
    assert screen.take_message() == ()
