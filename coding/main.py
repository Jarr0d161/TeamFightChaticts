from .settings import twitch_settings
from .tft_remote_control import TFTRemoteControl
from .twitch_connection import TwitchConnection
from .tft_overlay_ui import TFTRemoteControlOverlayUI
from .twitch_script import TFTTwitchBot


def main():
    tft_remote = TFTRemoteControl()
    twitch_connection = TwitchConnection(twitch_settings())
    twitch_chatbot = TFTTwitchBot(twitch_connection, tft_remote)
    overlay_ui = TFTRemoteControlOverlayUI(twitch_chatbot.start_bot, twitch_chatbot.stop_bot)
    overlay_ui.display_as_daemon()


if __name__ == '__main__':
    main()
