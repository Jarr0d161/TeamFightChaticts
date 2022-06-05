import socket
from typing import List, Callable
from dataclasses import dataclass, field

from .settings import TwitchSettings
from .tft_command import TFTCommand


@dataclass
class TwitchConnection:
    settings: TwitchSettings
    irc: socket.socket=field(init=False, default=None)
    msg_listeners: List[Callable[[str], None]]=field(init=False, default_factory=lambda: list())
    encoding: str='utf-8'
    buffer_size: int=1024

    def register_message_listener(self, listener: Callable[[str], None]):
        self.msg_listeners.append(listener)

    def connect_to_server(self):
        SUCCESS_TEXT = "End of /NAMES list"

        irc = socket.socket()
        irc.connect((self.settings.SERVER, self.settings.PORT))

        auth_msg = (
            f'PASS {self.settings.password}\n'
            f'NICK {self.settings.chatbot_name}\n'
            f'JOIN #{self.settings.channel}\n'
        )
        irc.send(auth_msg.encode(self.encoding))

        line = ''
        while SUCCESS_TEXT not in line:
            buffer = irc.recv(self.buffer_size).decode(self.encoding)
            line = buffer.split("\n")[-1]

        self.irc = irc

    def receive_messages_as_daemon(self, is_term_requested: Callable[[], bool]=lambda: False):
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode(self.encoding))

        is_ping_msg = lambda msg: "PING :tmi.twitch.tv" in msg
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
            if any(map(lambda line: is_ping_msg(line), lines)):
                self._send_twitch_pong()
            lines = [line for line in lines if not is_ping_msg(line)]

            messages = [self._parse_message_from_line(line) for line in lines]
            commands = [TFTCommand(cmd.lower()) for cmd in messages]

            for cmd in commands:
                self._notify_listeners(cmd)

            if is_term_requested():
                self.irc.close()
                break

    def _send_twitch_pong(self):
        msg = "PONG :tmi.twitch.tv\r\n".encode(self.encoding)
        self.irc.send(msg)

    def _parse_message_from_line(self, line: str) -> str:
        try:
            colons = line.count(":")
            line_parts = line.split(":", colons)
            user = line_parts[colons-1].split("!", 1)[0]
            message = line_parts[2] if len(line_parts) >= 3 else ""
            return message
        except:
            return ""

    def _notify_listeners(self, tft_cmd: TFTCommand):
        for listener in self.msg_listeners:
            listener(tft_cmd)
