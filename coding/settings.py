import os
from typing import Dict, Any
from dataclasses import dataclass
import pandas as pd


# TODO: translations for 'loadingComplete' are missing!!!
# TODO: translations for 'foundCommand' are missing!!!
# TODO: translations for 'commandWontRepeat' are missing!!!
gui_output_dict_english = {
    "ui_title": "TeamFightChaticts by Flanivia & Jarr0d",
    "start_button_text": "Start",
    "stop_button_text": "Stop",
    "launch_usage": "With the start button the twitchbot starts its work.",
    "auth_usage": "Enter auth for Twitch in config in the style auth=oauth:... and channel=channelname",
    "msg_pool_count": "Message pool (count):",
    "start": "Bot Started",
    "stop": "Bot Stopped",
    "close": "Bot Closing"
}


gui_output_dict_deutsch = {
    "ui_title": "TeamFightChaticts by Flanivia & Jarr0d",
    "start_button_text": "Start",
    "stop_button_text": "Stop",
    "launch_usage": "Mit dem Start Button beginnt der Twitchbot seine Arbeit.",
    "auth_usage": "Auth für Twitch in config eintragen im Stil auth=oauth:... und channel=channelname",
    "msg_pool_count": "Nachrichten Pool (Anzahl):",
    "start": "Bot gestartet",
    "stop": "Bot gestoppt",
    "close": "Bot wird geschlossen"
}


def read_config(config_filepath: str='../config/config.txt') -> pd.DataFrame:
    # TODO: replace this with JSON
    data = pd.read_csv(config_filepath, sep="=", index_col=0, header=None)
    data.columns = ["value"]
    return data


def tesseract_file_path() -> str:
    confList = read_config()
    return os.path.join(confList.loc['tesseract'][0], 'tesseract.exe')


def selected_language() -> str:
    confList = read_config()
    return confList.loc["language"]["value"]


def ui_settings_of_selected_language() -> Dict[Any, str]:
    language = selected_language()
    if language == "de":
        return gui_output_dict_deutsch
    elif language == "en":
        return gui_output_dict_english


@dataclass
class TwitchSettings:
    password: str
    channel: str
    SERVER: str = "irc.twitch.tv"
    PORT: int = 6667
    chatbot_name: str = "TeamFightChaticts"


def twitch_settings() -> TwitchSettings:
    confList = read_config()
    password = confList.loc['auth'][0]
    channel = confList.loc['channel'][0]
    return TwitchSettings(password, channel)
