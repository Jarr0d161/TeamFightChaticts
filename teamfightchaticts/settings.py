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


class AppSettings:
    def tesseract_rootdir(self) -> str:
        return self._app_settings()['tesseract_rootdir']

    def ui_settings_of_selected_language(
            self, translations_file: str='./config/translations_%LANG%.json') -> Dict[str, str]:
        lang = self._app_settings()['language']
        translations_file = translations_file.replace('%LANG%', lang)
        with open(translations_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def twitch_settings(self) -> TwitchSettings:
        twitch_conn = self._app_settings()['twitch_connection']
        return TwitchSettings(
            twitch_conn['server'],
            twitch_conn['port'],
            twitch_conn['channel'],
            twitch_conn['chatbot_name'],
            twitch_conn['password'])

    def tft_overlay_positions(self) -> Dict[str, Any]:
        return self._app_settings()['tft_overlay_positions']

    def _app_settings(self, config_file: str='./config/app_settings.json') -> Dict[str, Any]:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
