import json
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class TwitchSettings:
    server: str
    port: int
    channel: str
    chatbot_name: str
    password: str


def app_settings(config_file: str = "./config/app_settings.json") -> Dict[str, Any]:
    with open(config_file, "r") as file:
        return json.load(file)


def tesseract_rootdir() -> str:
    return app_settings()["tesseract_rootdir"]


def ui_settings_of_selected_language(
    translations_file: str = f"./config/translations_%LANG%.json",
) -> Dict[str, str]:
    lang = app_settings()["language"]
    translations_file = translations_file.replace("%LANG%", lang)
    with open(translations_file, "r") as file:
        return json.load(file)


def twitch_settings() -> TwitchSettings:
    twitch_conn = app_settings()["twitch_connection"]
    return TwitchSettings(
        twitch_conn["server"],
        twitch_conn["port"],
        twitch_conn["channel"],
        twitch_conn["chatbot_name"],
        twitch_conn["password"],
    )


def tft_overlay_positions() -> Dict[str, Any]:
    return app_settings()["tft_overlay_positions"]
