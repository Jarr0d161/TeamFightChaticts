import math
from typing import Tuple, List
import socket
import threading
import pyautogui
import time
import collections

from .settings import read_config
from .tft_screen_capture import capture_level, capture_gold, capture_item_locations


class TwitchBot:

    def __init__(self, chaos=False, pool=10):
        """
        Config laden
        """
        pyautogui.FAILSAFE = False

        self.chaos = chaos
        self.voll = False

        """
        Mapping für Brettfelder
        """
        self.reihe1=[(580,670),(710,670),(840,670),(970,670),(1100,670),(1230,670),(1360,670)]
        self.reihe2=[(530,590),(660,590),(790,590),(900,590),(1025,590),(1150,590),(1275,590)]
        self.reihe3=[(610,515),(730,515),(850,515),(965,515),(1080,515),(1200,515),(1315,515)]
        self.reihe4=[(560,430),(680,430),(790,430),(905,430),(1025,430),(1140,430),(1250,430)]
        self.reihe5=[(580,370),(710,370),(840,370),(970,370),(1100,370),(1230,370),(1340,370)]
        self.reihe6=[(560,315),(660,315),(790,315),(900,315),(1025,315),(1150,315),(1310,315)]
        self.reihe7=[(550,240),(730,240),(850,240),(965,240),(1080,240),(1200,240),(1315,240)]
        self.reihe8=[(590,175),(680,175),(790,175),(905,175),(1025,175),(1140,175),(1250,175)]
        self.banklist=[(420,780),(540,780),(660,780),(780,780),(900,780),(1020,780),(1140,780),(1260,780),(1380,780)]
        self.augmentlist= [(590,500),(960,500),(1320,500)]
        self.Rowlist= [self.banklist,self.reihe1,self.reihe2,self.reihe3,self.reihe4,self.reihe5,self.reihe6,self.reihe7,self.reihe8]    
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
        self.messagelist=[]
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

    def decodeString(self, partStr):
        try:
            x = str(partStr[0:1])
            y = int(partStr[1:2])
            if y < 8:
                if x.startswith('w'):
                    return self.banklist[y-1]
                if x.startswith('l'):
                    return self.reihe1[y-1]
                if x.startswith('b'):
                    return self.reihe2[y-1]
                if x.startswith('g'):
                    return self.reihe3[y-1]
                if x.startswith('r'):
                    return self.reihe4[y-1]
            if "w8" in partStr or "w9" in partStr:
                return self.banklist[y-1]
        except:
            print("Konnte nicht ausgeführt werden")
            self.message=""

    def get_items(self) -> list:
        search_box = (500, 200, 1375, 725)
        item_locs = capture_item_locations(search_box)
        len_matches = len(item_locs)

        if not len_matches:
            return None

        loc = self.filter_closeby_points(item_locs, 10)
        offset = 30
        omatches = []

        for pt in loc:
            omatches.append((pt[0] + search_box[0] + offset, pt[1] + search_box[1] + offset))

        return omatches[:4] if len(omatches) > 4 else omatches

    def filter_closeby_points(self, points: List[Tuple[int, int]], critical: int) -> List[Tuple[int, int]]:
        distances = [((i, j), math.dist(points[i], points[j]))
                     for i in range(points) for j in range(i)]
        relevant_edges = [edge for (edge, dist) in distances if dist >= critical]
        relevant_point_ids = set([e[0] for e in relevant_edges] + [e[1] for e in relevant_edges])
        return [points[id] for id in relevant_point_ids]

    def clickItems(self, locations: List[Tuple[int, int]]):
        for loc in locations:
            pyautogui.click(loc[0],loc[1], button='right')
            pyautogui.mouseUp(button='right')
            time.sleep(3)
        pyautogui.click(470, 650, button='right')
        pyautogui.mouseUp(button='right')
        self.clickIn()
    
    def clickIn(self):
        pyautogui.click(960,250, button='left')
        pyautogui.mouseUp(button='left')


    def addMessage(self, message):
        self.messagelist.append(message)
        print(self.messagelist)

        if collections.Counter(self.messagelist)[message] == self.counter:
            self.rein = True
            self.voll = True
        else:
            self.message = ""

    def joinchat(self):
        Loading = True
        while Loading:
            readbuffer_join = self.irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            print(readbuffer_join)
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = self.loadingComplete(line)

    def loadingComplete(self,line) -> bool:
        is_load_complete = "End of /NAMES list" not in line
        if not is_load_complete:
            print("TwitchBot ist am Start in " + self.CHANNEL + "' Channel!")
        return is_load_complete

    def getUser(self, line) -> str:
        colons = line.count(":")
        colonless = colons-1
        separate = line.split(":", colons)
        user = separate[colonless].split("!", 1)[0]
        return user

    def getMessage(self, line) -> str:
        try:
            colons = line.count(":")
            message = (line.split(":", colons))[2]
        except:
            message = ""
        return message

    def handle_shop_cmd(self, message: str):
        self.clickIn()
        z = int(message[4:]) - 1
        pyautogui.click(self.shoplist[z], button='left')
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_shop_cmd(self, message: str) -> bool:
        return message.startswith('shop') \
            and message[-1].isdigit() \
            and len(message) < 6 \
            and 0 < int(message[-1]) < 6

    def handle_augment_cmd(self, message: str):
        self.clickIn()
        selected_augment = self.augmentlist[int(message[3])-1]
        pyautogui.click(selected_augment)
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_augment_cmd(self, message: str) -> bool:
        return message.startswith('aug') \
            and message[-1].isdigit() \
            and len(message) < 5 \
            and 0 < int(message[-1]) < 4

    def handle_lock_or_unlock_cmd(self, message: str):
        self.clickIn()
        pyautogui.click(1450, 900, button='left')
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_lock_or_unlock_cmd(self, message: str) -> bool:
        return message in ['lock', 'unlock']

    def handle_karussell_cmd(self, message: str):
        self.clickIn()
        pyautogui.click(950, 370, button='right')
        pyautogui.mouseUp(button='right')
        self.reset_vars()

    def is_karussell_cmd(self, message: str) -> bool:
        return message == "now"

    def handle_collect_cmd(self, message: str):
        self.clickIn()
        items = self.get_items()
        print('Items:', items)
        if items:
            t2 = threading.Thread(target = self.clickItems, args=(items,))
            t2.start()
        self.reset_vars()

    def is_collect_cmd(self, message: str) -> bool:
        return message == 'collect'

    def handle_levelup_cmd(self, message: str):
        level = capture_level()
        gold = capture_gold()
        if not gold or not level:
            return
        act_xp, total_xp = level

        # determine clicks required to levelup
        # lvl guaruntees levelup for next rount, 
        xp_diff_to_level = total_xp - act_xp
        levelup_clicks = math.ceil(xp_diff_to_level / 4)
        levelup_clicks -= 1 if message == 'lvl' and xp_diff_to_level % 4 <= 2 else 0
        print(f'{act_xp} von {total_xp} XP, Kosten: {levelup_clicks * 4} Gold')

        pyautogui.moveTo(375, 960)
        while levelup_clicks > 0 and levelup_clicks * 4 <= gold:
            pyautogui.mouseDown(button="left")
            pyautogui.mouseUp(button="left")
            levelup_clicks -= 1

        self.clickIn()            
        self.reset_vars()

    def is_levelup_cmd(self, message: str) -> bool:
        return message in ['lvl', 'lvlup']

    def handle_roll_cmd(self, message: str):
        pyautogui.click(375,1045)
        pyautogui.mouseUp(button="left")
        self.clickIn()
        self.reset_vars()

    def is_roll_cmd(self, message: str) -> bool:
        return message in ['roll', 'reroll']

    def handle_sellw_cmd(self, message: str):
        self.clickIn()
        z = self.decodeString(message[4:6])
        pyautogui.moveTo(z)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(self.shoplist[2])
        pyautogui.mouseUp(button='left')
        pyautogui.moveTo(z)
        self.reset_vars()

    def is_sellw_cmd(self, message: str) -> bool:
        return message.startswith('sellw') and len(message) < 7 \
            and message[4:5] in self.farblist \
            and message[-1].isdigit() and int(message[-1]) > 0 \
            and (message[4:6] == "w8" or message[4:6] == "w9" or 0 < int(message[-1]) < 8)

    def handle_place_unit_cmd(self, message: str):
        self.clickIn()
        origin = str(message[0:2])
        aim = str(message[2:4]) 
        pyautogui.moveTo(self.decodeString(origin))
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(self.decodeString(aim))
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_place_unit_cmd(self, message: str) -> bool:
        return len(message) < 5 and message[0:1] in self.farblist and message[1:2].isnumeric() \
            and message[2:3] in self.farblist and message[3:4].isnumeric() \
            and (message[2:4] == "w8" or message[2:4] == "w9" or 1 <= int(message[-1]) <= 7) \
            and (message[0:2] == "w8" or message[0:2] == "w9" or 1 <= int(message[1:2]) <= 7)

    def handle_collect_items_cmd(self, message: str):
        self.clickIn()
        z = int(message[3:])
        temp = ((self.Rowlist[z])[0][0] - 100, (self.Rowlist[z])[0][1])
        pyautogui.click(temp,button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(2)
        temp = ((self.Rowlist[z])[6][0] + 100, (self.Rowlist[z])[6][1])
        print(temp, type(temp))
        pyautogui.click(temp,button='right')
        pyautogui.mouseUp(button='right')
        self.reset_vars()

    def is_collect_items_cmd(self, message: str) -> bool:
        return message.startswith('row') and len(message) < 5 \
            and message[-1].isdigit() and 0 < int(message[-1]) < 9

    def handle_attach_item_cmd(self, message: str):
        self.clickIn()
        slot = str(message[0:1])
        if slot == "a":
            pyautogui.moveTo(self.itemlist[0])
        if slot == "b":
            pyautogui.moveTo(self.itemlist[1])
        if slot == "c":
            pyautogui.moveTo(self.itemlist[2])
        if slot == "d":
            pyautogui.moveTo(self.itemlist[3])
        if slot == "e":
            pyautogui.moveTo(self.itemlist[4])
        if slot == "f":
            pyautogui.moveTo(self.itemlist[5])
        if slot == "g":
            pyautogui.moveTo(self.itemlist[6])
        if slot == "h":
            pyautogui.moveTo(self.itemlist[7])
        if slot == "i":
            pyautogui.moveTo(self.itemlist[8])
        if slot == "j":
            pyautogui.moveTo(self.itemlist[9])
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(self.decodeString(message[1:]))
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_attach_item_cmd(self, message: str) -> bool:
        return message[0:1] in self.itemWhitelist and message[1:2] in self.farblist \
            and len(message) < 4 and message[-1].isdigit() \
            and message[1:3] == "w8" or message[1:3] == "w9" or 0 < int(message[-1]) < 8

    def gamecontrol(self, message=''):
        self.message = message = message.lower()

        if not self.rein and not self.chaos:
            self.addMessage(message)

        elif self.is_shop_cmd(message):
            self.handle_shop_cmd(message)

        elif self.is_augment_cmd(message):
            self.handle_augment_cmd(message)

        elif self.is_lock_or_unlock_cmd(message):
            self.handle_lock_or_unlock_cmd(message)

        elif self.is_karussell_cmd(message):
            self.handle_karussell_cmd(message)

        elif self.is_collect_cmd(message):
            self.handle_collect_cmd(message)

        elif self.is_levelup_cmd(message):
            self.handle_levelup_cmd(message)

        elif self.is_roll_cmd(message):
            self.handle_roll_cmd(message)

        elif self.is_sellw_cmd(message):
            self.handle_sellw_cmd(message)
    
        elif self.is_place_unit_cmd(message):
            self.handle_place_unit_cmd(message)
                  
        elif self.is_collect_items_cmd(message):
            self.handle_collect_items_cmd(message)

        elif self.is_attach_item_cmd(message):
            self.handle_attach_item_cmd(message)
        
        if self.voll and not self.chaos:
            if message != self.old_message:
                print("Erkannter Befehl:", message)
                self.rein = True
                self.voll = False
                self.messagelist.clear()
                self.old_message = message
                self.gamecontrol(message)
            else:
                print('Befehl wird nicht wiederholt!')
                self.messagelist = list(filter((message).__ne__, self.messagelist))
                print(self.messagelist)
                self.reset_vars()
                
                    
    def start_bot(self):
        self.stop_thread.clear()
        self.thread = threading.Thread(target=self.twitch)
        self.thread.start()
    

    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None
    
    def twitch(self):
        self.joinchat()
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
        
        while True:
            
            try:
                readbuffer = self.irc.recv(1024).decode()
            except:
                readbuffer = ""
            for line in readbuffer.split("\r\n"):
                if line == "":
                    continue
                if "PING :tmi.twitch.tv" in line:
                    print(line)
                    msgg = "PONG :tmi.twitch.tv\r\n".encode()
                    self.irc.send(msgg)
                    print(msgg)
                    continue
                else:
                    try:                        
                        self.user = self.getUser(line)
                        self.message = self.getMessage(line)
                        print(self.user + " : " + self.message)                      
                        self.gamecontrol(self.message)                        
                    except Exception:
                        pass

            if self.stop_thread.is_set():
                self.irc.close()
                break


if __name__ =='__main__':
    bot = TwitchBot(chaos=False, pool=1)
    t1 = threading.Thread(target = bot.twitch())
    t1.start()
