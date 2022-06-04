from typing import List
import socket
import threading
import pyautogui
import collections

from .settings import read_config
from .tft_remote_control import TFTRemoteControl

class TwitchBot:

    def __init__(self, chaos=False, pool=10):
        """
        Config laden
        """
        pyautogui.FAILSAFE = False

        self.chaos = chaos
        self.voll = False

        self.tft_remote_control = TFTRemoteControl

        """
        Mapping für Brettfelder
        """
        self.row_1=[(580,670),(710,670),(840,670),(970,670),(1100,670),(1230,670),(1360,670)]
        self.row_2=[(530,590),(660,590),(790,590),(900,590),(1025,590),(1150,590),(1275,590)]
        self.row_3=[(610,515),(730,515),(850,515),(965,515),(1080,515),(1200,515),(1315,515)]
        self.row_4=[(560,430),(680,430),(790,430),(905,430),(1025,430),(1140,430),(1250,430)]
        # self.reihe5=[(580,370),(710,370),(840,370),(970,370),(1100,370),(1230,370),(1340,370)]
        # self.reihe6=[(560,315),(660,315),(790,315),(900,315),(1025,315),(1150,315),(1310,315)]
        # self.reihe7=[(550,240),(730,240),(850,240),(965,240),(1080,240),(1200,240),(1315,240)]
        # self.reihe8=[(590,175),(680,175),(790,175),(905,175),(1025,175),(1140,175),(1250,175)]
        # info: positions on opponent's side of the board are never used to place own units
        self.bench=[(420,780),(540,780),(660,780),(780,780),(900,780),(1020,780),(1140,780),(1260,780),(1380,780)]
        self.augmentlist= [(590,500),(960,500),(1320,500)]
        self.Rowlist= [self.bench,self.row_1,self.row_2,self.row_3,self.row_4]#,self.reihe5,self.reihe6,self.reihe7,self.reihe8]
        self.itemlist = [(290,755),(335,725),(310,705),(350,660),(410,665),(325,630),(385,630),(445,630),(340,590),(395,590)]
        self.shoplist=[(570,1000),(770,1000),(970,1000),(1170,1000),(1370,1000)]
        self.comlist = [(370,980),(370,1060)]
        self.farblist=["w","l","b","g","r"]
        self.itemWhitelist = ["a","b","c","d","e","f","g","h","i","j"]

        """
        IRC Verbindungaufbauen
        """
        self.confList = read_config()
        self.SERVER = "irc.twitch.tv"
        self.PORT = 6667
        self.BOT = "TeamFightChaticts"
        self.PASS = self.confList.loc['auth'][0]
        self.CHANNEL = self.confList.loc['channel'][0]
        self.OWNER = self.confList.loc['channel'][0] # TODO: why not use CHANNEL for both?

        self.irc = socket.socket()
        self.irc.connect((self.SERVER, self.PORT))
        self.irc.send(f'PASS {self.PASS}\nNICK {self.BOT}\nJOIN #{self.CHANNEL}\n'.encode())

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
                Loading = self.loadingComplete(line)

    def loadingComplete(self, line: str) -> bool:
        is_load_complete = "End of /NAMES list" not in line
        if not is_load_complete:
            print("TwitchBot ist am Start in " + self.CHANNEL + "' Channel!")
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

    def start_bot(self):
        self.stop_thread.clear()
        self.thread = threading.Thread(target=self.twitch)
        self.thread.start()


    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None

    def twitch(self):
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
                    print("Erkannter Befehl:", message)
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
                    print('Befehl wird nicht wiederholt!')
                    self.messagelist = list(filter((message).__ne__, self.messagelist))
                    print(self.messagelist)
                    self.reset_vars()

        except Exception:
            pass


if __name__ =='__main__':
    bot = TwitchBot(chaos=False, pool=1)
    t1 = threading.Thread(target = bot.twitch())
    t1.start()
