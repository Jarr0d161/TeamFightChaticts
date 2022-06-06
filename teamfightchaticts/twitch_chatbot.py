import threading
from time import sleep
from typing import Dict
from dataclasses import dataclass, field

from teamfightchaticts.tft_command import TFTCommand
from teamfightchaticts.twitch_connection import TwitchConnection
from teamfightchaticts.tft_remote_control import TFTRemoteControl


@dataclass
class TwitchTFTChatbotState:
    last_cmd: TFTCommand = TFTCommand("")
    cmd_counts: Dict[TFTCommand, int] = field(default_factory=lambda: dict())
    pool: int = 10

    def update_state(self, tft_cmd: TFTCommand):
        self.cmd_counts[tft_cmd] += 1

    def reset_counts(self):
        self.last_cmd = self.cmd_to_execute
        self.cmd_counts = dict()

    @property
    def cmd_to_execute(self) -> TFTCommand:
        return next(
            filter(lambda cmd: self.cmd_counts[cmd] >= self.pool, self.cmd_counts), None
        )


@dataclass
class TwitchTFTChatbot:
    connection: TwitchConnection
    tft_remote_control: TFTRemoteControl
    state: TwitchTFTChatbotState = TwitchTFTChatbotState()
    thread: threading.Thread = field(init=False, default=None)
    shutdown_requested: bool = False

    def start_bot(self, pool_size: int):
        if self.shutdown_requested:
            return
        self.state.pool = pool_size
        self.shutdown_requested = False
        self.thread = threading.Thread(target=self.receive_twitch_messages)

    def stop_bot(self):
        self.shutdown_requested = True
        while self.thread.is_alive():
            sleep(0.1)
        self.shutdown_requested = False

    def receive_twitch_messages(self):
        self.connection.connect_to_server()
        self.connection.register_message_listener(self.process_tft_cmd)
        self.connection.receive_messages_as_daemon(lambda: self.shutdown_requested)

    def process_tft_cmd(self, tft_cmd: TFTCommand):
        self.state.update_state(tft_cmd)
        cmd_exec = self.state.cmd_to_execute

        # no command to execute
        if not cmd_exec:
            return

        # same command twice
        if cmd_exec == self.state.last_cmd:
            self.state.last_cmd = TFTCommand("")
            return

        # command is ok, go execute it
        self.tft_remote_control.execute_cmd(cmd_exec)
        self.state.reset_counts()
