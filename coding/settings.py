import os
from typing import Dict, Any
import pandas as pd


# TODO: translations for 'loadingComplete' are missing!!!
# TODO: translations for 'foundCommand' are missing!!!
# TODO: translations for 'commandWontRepeat' are missing!!!
gui_output_dict_english = {
    "256": "With the start button the twitchbot starts its work.",
    "253": "Enter auth for Twich in config in the style auth=oauth:... and channel=channelname",
    "459": "Message pool (count):",
    "start": "Bot Started",
    "stop": "Bot Stopped",
    "close": "Bot Closing"
}


gui_output_dict_deutsch = {
    "256": "Mit dem Start Button beginnt der Twitchbot seine Arbeit.",
    "253": "Auth für Twich in config eintragen im Stil auth=oauth:... und channel=channelname",
    "459": "Nachrichten Pool (Anzahl):",
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


def twitch_password() -> str:
    confList = read_config()
    return confList.loc['auth'][0]


def twitch_channel_to_be_observed() -> str:
    confList = read_config()
    return confList.loc['channel'][0]
