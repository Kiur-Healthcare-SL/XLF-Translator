from support.app_driver import started


def test_the_app_starts_without_exceptions():
    app = started()
    assert not app.exception
