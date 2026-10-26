from collections.abc import MutableMapping

SCREEN_KEY = "xlf_translator.screen"
RETURN_KEY = "xlf_translator.return_screen"
FINAL_EXPORT_KEY = "xlf_translator.final_export_requested"
UPLOAD_GENERATION_KEY = "xlf_translator.upload_generation"
MESSAGE_KEY = "xlf_translator.message"
TRANSLATE = "translate"
FINISH = "finish"
GUIDE = "guide"


class ScreenState:
    """Which screen is showing, and what the screens remember between reruns."""

    def __init__(self, state: MutableMapping):
        self._state = state

    def current(self) -> str:
        return self._state.get(SCREEN_KEY, TRANSLATE)

    def show(self, screen: str) -> None:
        self._state[SCREEN_KEY] = screen

    def open_guide(self) -> None:
        self._state[RETURN_KEY] = self.current()
        self.show(GUIDE)

    def close_guide(self) -> None:
        self.show(self._state.get(RETURN_KEY, TRANSLATE))

    def request_final_export(self) -> None:
        self._state[FINAL_EXPORT_KEY] = True

    def final_export_requested(self) -> bool:
        return self._state.get(FINAL_EXPORT_KEY, False)

    def upload_key(self) -> str:
        return f"upload-{self._state.get(UPLOAD_GENERATION_KEY, 0)}"

    def start_over(self) -> None:
        self._state[UPLOAD_GENERATION_KEY] = self._state.get(UPLOAD_GENERATION_KEY, 0) + 1
        self._state[FINAL_EXPORT_KEY] = False
        self.show(TRANSLATE)

    def tell(self, message: tuple[str, ...]) -> None:
        self._state[MESSAGE_KEY] = message

    def take_message(self) -> tuple[str, ...]:
        return self._state.pop(MESSAGE_KEY, ())
