import re
import socket
import threading
import collections
from typing import List, Callable
from dataclasses import dataclass, field

from .settings import *
from .tft_remote_control import TFTRemoteControl


@dataclass
class TwitchConnection:
    settings: TwitchSettings
    irc: socket.socket=field(init=False, default=None)
    msg_filters: List[str]=field(init=False, default_factory=lambda: list())
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
            buffer = irc.recv(self.buffer_size)
            buffer = buffer.decode(self.encoding)
            print(buffer)
            line = buffer.split("\n")[-1]

        self.irc = irc

    def receive_messages_as_daemon(self, is_term_requested: Callable[[], bool]=lambda: False):
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode(self.encoding))

        is_pattern_match = lambda msg, pattern: re.match(pattern, msg) is not None
        is_valid_msg = lambda msg: any(map(lambda f: is_pattern_match(msg, f), self.msg_filters))
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
            messages = list(filter(lambda msg: is_valid_msg(msg), messages))

            for msg in messages:
                self._notify_listeners(msg)

            if is_term_requested():
                self.irc.close()
                break

    def _send_twitch_pong(self):
        msg = "PONG :tmi.twitch.tv\r\n".encode(self.encoding)
        self.irc.send(msg)
        print(msg)

    def _parse_message_from_line(self, line: str) -> str:
        # TODO: apply a regex as pre-pass to ensure that this logic doesn't crash
        colons = line.count(":")
        line_parts = line.split(":", colons)
        user = line_parts[colons-1].split("!", 1)[0]
        message = line_parts[2] if len(line_parts) >= 3 else ""
        print(f'{user} : {message}')
        return message

    def _notify_listeners(self, message: str):
        for listener in self.msg_listeners:
            listener(message)


class TwitchBot:
    def __init__(self, connection: TwitchConnection, chaos: bool=False):
        self.chaos = chaos
        self.voll = False

        self.connection = connection
        self.tft_remote_control = TFTRemoteControl()
        self.ui_settings = ui_settings_of_selected_language()
        self.twitch_setings = twitch_settings()

        # TODO: put the chatbot state into a dataclass
        self.message = ""
        self.old_message = ''
        self.counter = 0
        self.messagelist: List[str] = []
        self.rein = False
        self.thread = None
        self.stop_thread = threading.Event()

    def reset_vars(self):
        #self.messagelist.clear()
        self.voll = False
        self.rein = False
        self.message = ""

    def add_message(self, message):
        self.messagelist.append(message)
        print(self.messagelist)

        if collections.Counter(self.messagelist)[message] == self.counter:
            self.rein = True
            self.voll = True
        else:
            self.message = ""

    def start_bot(self, pool_size: int):
        self.stop_thread.clear()
        self.counter = pool_size
        self.thread = threading.Thread(target=self.receive_twitch_messages)
        self.thread.start()

    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None

    def receive_twitch_messages(self):
        self.connection.connect_to_server()
        self.connection.register_message_listener(self.process_tft_cmd)
        self.connection.receive_messages_as_daemon()
        # TODO: use the is_term_requested callback to gracefully exit chatbot thread

    def process_tft_cmd(self, message: str):
        self.message = message = message.lower()

        if not self.rein and not self.chaos:
            self.add_message(message)
        else:
            self.tft_remote_control.gamecontrol(message)
            self.reset_vars()

        if self.voll and not self.chaos:
            if message != self.old_message:
                print(f"{self.ui_settings['foundCommand']} {message}")
                self.rein = True
                self.voll = False
                self.messagelist.clear()
                self.old_message = message
                self.message = message = message.lower()
                if not self.rein and not self.chaos:
                    self.add_message(message)
                else:
                    self.tft_remote_control.gamecontrol(message)
                    self.reset_vars()
            else:
                print(self.ui_settings['commandWontRepeat'])
                self.messagelist = list(filter((message).__ne__, self.messagelist))
                print(self.messagelist)
                self.reset_vars()
