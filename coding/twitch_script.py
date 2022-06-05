from typing import List, Tuple
import socket
import threading
import collections

from .settings import *
from .tft_remote_control import TFTRemoteControl


class TwitchBot:
    def __init__(self, chaos=False):
        self.chaos = chaos
        self.voll = False

        self.ui_settings = ui_settings_of_selected_language()
        self.tft_remote_control = TFTRemoteControl()
        self.twitch_channel, self.irc = self.connect_to_twitch()

        # TODO: put the chatbot state into a dataclass
        self.message = ""
        self.old_message = ''
        self.user = ""
        self.pool = pool
        print("Pool ist bei: "+str(self.pool))
        self.counter = self.pool
        self.tempCount = 0
        self.messagelist: List[str] = []
        self.rein = False
        self.diff = 0
        self.bCom = False
        self.stopRunning = False
        self.lockActivated = False
        self.thread = None
        self.stop_thread = threading.Event()

    def connect_to_twitch(self) -> Tuple[str, socket.socket]:
        # TODO: put all twitch settings in one dataclass
        SERVER = "irc.twitch.tv"
        PORT = 6667
        BOT = "TeamFightChaticts"
        PASS = twitch_password()
        # OWNER = twitch_channel_owner()
        channel = twitch_channel_to_be_observed()

        irc = socket.socket()
        irc.connect((SERVER, PORT))
        irc.send(f'PASS {PASS}\nNICK {BOT}\nJOIN #{channel}\n'.encode())
        return irc, channel

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

    def join_chat(self):
        Loading = True
        while Loading:
            readbuffer_join = self.irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            print(readbuffer_join)
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = self.loading_omplete(line)

    def loading_omplete(self, line: str) -> bool:
        is_load_complete = "End of /NAMES list" not in line
        if not is_load_complete:
            print(f"{self.ui_settings['loadingComplete']} {self.twitch_channel}' Channel!")
        return is_load_complete

    def parse_submitting_user(self, line: str) -> str:
        colons = line.count(":")
        colonless = colons-1
        separate = line.split(":", colons)
        user = separate[colonless].split("!", 1)[0]
        return user

    def parse_tft_command(self, line: str) -> str:
        try:
            colons = line.count(":")
            message = (line.split(":", colons))[2]
        except:
            message = ""
        return message

    def start_bot(self, pool_size: int):
        self.stop_thread.clear()
        self.thread = threading.Thread(target=self.twitch)
        self.thread.start()

    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None

    def twitch(self):
        # TODO: invert dependency between overlay ui and chat bot, decouple using callback funcions

        self.join_chat()
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode())

        while True:
            self.process_twitch_messages()

            if self.stop_thread.is_set():
                self.irc.close()
                break

    def process_twitch_messages(self):
        try:
            readbuffer = self.irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            if "PING :tmi.twitch.tv" in line:
                # print(line)
                self.send_twitch_pong()
                continue
            else:
                # TODO: add a TFT command parser to ensure that the command is valid -> simplify error handing
                self.execute_tft_command(line)

    def send_twitch_pong(self):
        msgg = "PONG :tmi.twitch.tv\r\n".encode()
        self.irc.send(msgg)
        print(msgg)

    def execute_tft_command(self, line: str):
        try:
            user = self.parse_submitting_user(line)
            message = self.parse_tft_command(line)
            print(f'{user} : {message}')

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

        except Exception:
            pass


if __name__ == '__main__':
    bot = TwitchBot(chaos=False, pool=1)
    t1 = threading.Thread(target = bot.twitch())
    t1.start()
