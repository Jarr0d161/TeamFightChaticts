from teamfightchaticts.settings import AppSettings
from teamfightchaticts.mouse_control import MouseControl
from teamfightchaticts.tft_screen_capture import TFTTesseractScreenCapture
from teamfightchaticts.tft_remote_control import TFTRemoteControl
from teamfightchaticts.twitch_connection import TwitchConnection
from teamfightchaticts.twitch_chatbot_launcher_ui import TwitchChatbotLauncherUI
from teamfightchaticts.twitch_chatbot import TwitchTFTChatbot


def main():
    config = AppSettings()
    mouse = MouseControl()
    tft_screen_capture = TFTTesseractScreenCapture(config.tesseract_rootdir())
    tft_remote = TFTRemoteControl(config.tft_overlay_positions(), tft_screen_capture, mouse)
    twitch_connection = TwitchConnection(config.twitch_settings())
    twitch_chatbot = TwitchTFTChatbot(twitch_connection, tft_remote)
    overlay_ui = TwitchChatbotLauncherUI(twitch_chatbot, config.ui_settings_of_selected_language())
    overlay_ui.display_as_daemon()


if __name__ == '__main__':
    main()
