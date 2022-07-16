from socket import socket
from typing import Tuple, List, Callable, Protocol
from dataclasses import dataclass, field

from teamfightchaticts.settings import TwitchSettings


class IrcSocket(Protocol):
    def connect(self, creds: Tuple[str, int]):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def recv(self, bufsize: int) -> bytes:
        raise NotImplementedError()

    def send(self, data: bytes) -> int:
        raise NotImplementedError()


@dataclass
class LineBuffer:
    remainder: str = ''
    sep: str = '\r\n'

    def process(self, text_buffer: str) -> List[str]:
        buffer_text = self.remainder + text_buffer
        lines = buffer_text.split(self.sep)
        self.remainder = lines[-1]
        lines.pop()
        return lines


def filter_pings(raw_lines: List[str]) -> Tuple[List[str], bool]:

    def is_ping_msg(msg: str) -> bool:
        return "PING :tmi.twitch.tv" in msg

    contains_ping = any(map(is_ping_msg, raw_lines))
    lines = [line for line in raw_lines if line and not is_ping_msg(line)]
    print("lines are:", lines)
    return lines, contains_ping


def parse_message_from_line(line: str) -> str:
    line_parts = line.split(":")
    return line_parts[2] if len(line_parts) >= 3 else ""


@dataclass
class TwitchConnection:
    # pylint: disable=bare-except, broad-except
    settings: TwitchSettings
    socket_factory: Callable[[], IrcSocket]=socket
    encoding: str='utf-8'
    buffer_size: int=1024
    timeout_seconds: int=60
    websocket: IrcSocket=field(init=False, default=None)
    msg_listeners: List[Callable[[str], None]]=field(init=False, default_factory=list)

    def register_message_listener(self, listener: Callable[[str], None]):
        self.msg_listeners.append(listener)

    def connect_to_server(self):
        websocket = self.socket_factory()

        websocket.connect((self.settings.server, self.settings.port))
        self._send_auth_message(websocket)
        self._wait_for_auth_complete(websocket)

        self.websocket = websocket

    def _send_auth_message(self, irc: IrcSocket):
        auth_msg = (
            f'PASS {self.settings.password}\n'
            f'NICK {self.settings.chatbot_name}\n'
            f'JOIN #{self.settings.channel}\n'
        )
        irc.send(auth_msg.encode(self.encoding))

    def _wait_for_auth_complete(self, websocket: IrcSocket):

        def found_end_of_auth(lines: List[str]) -> bool:
            success_text = "End of /NAMES list"
            return any(filter(lambda line: success_text in line, lines))

        lines = []
        line_buffer = LineBuffer()
        while not found_end_of_auth(lines):
            lines = line_buffer.process(self._read_next_buffer(websocket))

    def receive_messages_as_daemon(self, is_term_requested: Callable[[], bool]=lambda: False):
        self._request_listening_to_twitch_chat()
        line_buffer = LineBuffer()

        while not is_term_requested():
            buffer = self._read_next_buffer(self.websocket)
            lines = line_buffer.process(buffer)

            # handle ping-pong messages to keep the connection alive
            lines, send_pong = filter_pings(lines)
            if send_pong:
                self._send_twitch_pong()

            messages = [parse_message_from_line(line).lower() for line in lines]
            for msg in messages:
                self._notify_listeners(msg)

        self.websocket.close()

    def _request_listening_to_twitch_chat(self):
        self.websocket.send("CAP REQ :twitch.tv/tags\r\n".encode(self.encoding))

    def _read_next_buffer(self, websocket: IrcSocket) -> str:
        try:
            return websocket.recv(self.buffer_size).decode(self.encoding)
        except:
            return ''

    def _send_twitch_pong(self):
        msg = "PONG :tmi.twitch.tv\r\n".encode(self.encoding)
        self.websocket.send(msg)

    def _notify_listeners(self, msg: str):
        for listener in self.msg_listeners:
            listener(msg)
