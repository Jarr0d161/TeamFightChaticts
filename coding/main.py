from .settings import \
    tesseract_rootdir, tft_overlay_positions, \
    twitch_settings, ui_settings_of_selected_language
from .tft_screen_capture import TFTTesseractScreenCapture
from .tft_remote_control import TFTRemoteControl
from .twitch_connection import TwitchConnection
from .tft_overlay_ui import TFTRemoteControlOverlayUI
from .twitch_chatbot import TwitchTFTChatbot


def main():
    tft_screen_capture = TFTTesseractScreenCapture(tesseract_rootdir())
    tft_remote = TFTRemoteControl(tft_overlay_positions(), tft_screen_capture)
    twitch_connection = TwitchConnection(twitch_settings())
    twitch_chatbot = TwitchTFTChatbot(twitch_connection, tft_remote)
    overlay_ui = TFTRemoteControlOverlayUI(
        twitch_chatbot.start_bot, twitch_chatbot.stop_bot,
        ui_settings_of_selected_language())
    overlay_ui.display_as_daemon()


if __name__ == '__main__':
    main()
