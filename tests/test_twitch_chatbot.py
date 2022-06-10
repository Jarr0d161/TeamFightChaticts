from typing import Tuple
from dataclasses import dataclass
from teamfightchaticts.settings import AppSettings
from teamfightchaticts.twitch_connection import TwitchConnection


@dataclass
class IrcSocketMock:
    text_to_return: str
    text_received: str=''
    closed: bool=True
    buffer_id: int=0
    encoding: str='utf-8'

    def connect(self, _: Tuple[str, int]):
        self.closed = False

    def close(self):
        self.closed = True

    def recv(self, bufsize: int) -> bytes:
        text_enc = self.text_to_return.encode(self.encoding)
        start, end = self.buffer_id * bufsize, (self.buffer_id + 1) * bufsize
        self.buffer_id += 1
        return text_enc[start:min(end, len(text_enc))]

    def send(self, data: bytes) -> int:
        self.text_received += data.decode(self.encoding)


def test_should_connect_to_chat():
    conn_settings = AppSettings().twitch_settings()
    connection = TwitchConnection(conn_settings)
    text_to_return = "End of /NAMES list"
    connection.connect_to_server(lambda: IrcSocketMock(text_to_return))
    exp_text_buffer = (
        f'PASS {conn_settings.password}\n'
        f'NICK {conn_settings.chatbot_name}\n'
        f'JOIN #{conn_settings.channel}\n'
    )
    socket: IrcSocketMock = connection.irc
    assert socket.closed is False and socket.text_received == exp_text_buffer


def test_should_fail_connection_to_chat_with_timeout():
    pass


def test_should_disconnect_from_chat_gracefully():
    pass


def test_should_send_chat_pong():
    pass


def test_should_parse_tft_commands_from_chat_with_single_recv():
    pass


def test_should_parse_tft_commands_from_chat_replay_with_overlapping_recv_buffes():
    pass
