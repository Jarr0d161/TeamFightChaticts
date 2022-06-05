from .tft_overlay_ui import TFTRemoteControlOverlayUI
from .twitch_script import TwitchBot


def main():
    chatbot = TwitchBot()
    overlay_ui = TFTRemoteControlOverlayUI(chatbot.start_bot, chatbot.stop)
    overlay_ui.display_as_daemon()


if __name__ == '__main__':
    main()
