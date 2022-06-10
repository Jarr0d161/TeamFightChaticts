from socket import socket
from typing import Tuple, List, Callable, Protocol
from dataclasses import dataclass, field

from teamfightchaticts.settings import TwitchSettings


@dataclass
class TFTCommand(Protocol):
    cmd: str


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
class TwitchConnection:
    # pylint: disable=bare-except, broad-except
    settings: TwitchSettings
    irc: IrcSocket=field(init=False, default=None)
    msg_listeners: List[Callable[[TFTCommand], None]]=field(init=False, default_factory=lambda: [])
    encoding: str='utf-8'
    buffer_size: int=1024

    def register_message_listener(self, listener: Callable[[TFTCommand], None]):
        self.msg_listeners.append(listener)

    def connect_to_server(self, socket_factory: Callable[[], IrcSocket]=socket):
        irc = socket_factory()
        irc.connect((self.settings.server, self.settings.port))

        auth_msg = (
            f'PASS {self.settings.password}\n'
            f'NICK {self.settings.chatbot_name}\n'
            f'JOIN #{self.settings.channel}\n'
        )
        irc.send(auth_msg.encode(self.encoding))

        line = ''
        success_text = "End of /NAMES list"
        while success_text not in line:
            buffer = irc.recv(self.buffer_size).decode(self.encoding)
            line = buffer.split("\n")[-1]
        # TODO: add a timeout exception if Twitch doesn't respond

        self.irc = irc

    def receive_messages_as_daemon(self, is_term_requested: Callable[[], bool]=lambda: False):
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode(self.encoding))

        def is_ping_msg(msg: str) -> bool:
            return "PING :tmi.twitch.tv" in msg

        remainder = ''
        while True:
            try:
                # TODO: make sure this doesn't crash when processing all kinds of emoticons
                readbuffer = self.irc.recv(self.buffer_size).decode(self.encoding)
            except:
                readbuffer = ""
            lines = readbuffer.split("\r\n")
            lines[0] = remainder + lines[0]
            remainder = lines[-1]

            # handle ping-pong messages to keep the connection alive
            if any(map(is_ping_msg, lines)):
                self._send_twitch_pong()
            lines = [line for line in lines if not is_ping_msg(line)]

            messages = [TwitchConnection._parse_message_from_line(line) for line in lines]
            commands = [TFTCommand(cmd.lower()) for cmd in messages]

            for cmd in commands:
                self._notify_listeners(cmd)

            if is_term_requested():
                self.irc.close()
                break

    def _send_twitch_pong(self):
        msg = "PONG :tmi.twitch.tv\r\n".encode(self.encoding)
        self.irc.send(msg)

    @staticmethod
    def _parse_message_from_line(line: str) -> str:
        line_parts = line.split(":")
        return line_parts[2] if len(line_parts) >= 3 else ""

    def _notify_listeners(self, tft_cmd: TFTCommand):
        for listener in self.msg_listeners:
            listener(tft_cmd)
