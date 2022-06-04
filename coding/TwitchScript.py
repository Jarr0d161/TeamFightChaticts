import socket
import threading
import pyautogui
import time
import collections
import numpy as np
import pytesseract
from PIL import ImageGrab
import cv2
import os

import pandas as pd

def select_gui_output_language(language):
    if language == "de":
        return gui_output_dict_deutsch
    elif language == "en":
        return gui_output_dict_english

gui_output_dict_english = {
    "tesseractErr": "The path for Tesseract is not correct!",
    "pool": "Pool is at:",
    "decodeString": "Could not be executed",
    "loadingComplete": "Twitch bot runs at ",
    "foundCommand": "Found command: ",
    "commandWontRepeat": "Command will not be repeated",
}

gui_output_dict_deutsch = {
    "tesseractErr": "Der Pfad für Tesseract ist nicht korrekt!",
    "pool": "Pool ist bei:",
    "decodeString": "Konnte nicht ausgeführt werden",
    "loadingComplete": "TwitchBot ist am Start in ",
    "foundCommand": "Erkannter Befehl: ",
    "commandWontRepeat": "Befehl wird nicht wiederholt!",
}

class TwitchBot:

    def __init__(self, chaos=False, pool=10):
        
        """
        Config laden
        """
        pyautogui.FAILSAFE = False
        self.confList = TwitchBot.readConfig()
        self.guiOutput = select_gui_output_language(self.confList.loc["language"]["value"])

        self.chaos = chaos
        self.voll = False
        
        file_path = os.path.join(self.confList.loc['tesseract'][0], 'tesseract.exe')
        isExist = os.path.exists(file_path)
                
        if isExist: pytesseract.pytesseract.tesseract_cmd = file_path
        else: raise ValueError(self.guiOutput["tesseractErr"])
        
        
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
        self.SERVER = "irc.twitch.tv"
        self.PORT = 6667
        self.PASS = self.confList.loc['auth'][0]
    
        
        self.BOT = "TeamFightChaticts"
    
        #The channel you want to monitor
        self.CHANNEL = self.confList.loc['channel'][0]
        
        #Your account
        self.OWNER = self.confList.loc['channel'][0]
        
    
        self.irc = socket.socket()
        self.irc.connect((self.SERVER, self.PORT))
        self.irc.send((    "PASS " + self.PASS + "\n" +
                    "NICK " + self.BOT + "\n" +
                    "JOIN #" + self.CHANNEL + "\n").encode())
        
        """
        ...
        """
        self.message = ""
        self.old_message = ''
        self.user = ""
        self.pool = pool
        print(self.guiOutput['pool']+str(self.pool))
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

    
    @staticmethod
    def readConfig() -> pd.DataFrame:
        
        data = pd.read_csv('../config/config.txt', sep="=", index_col=0, header=None)
        data.columns = ["value"]
        return data  

    def resetVars(self):
        
        #self.messagelist.clear()
        self.voll = False
        self.rein = False
        self.message = ""


    def sendMessage(self, message):
        
            messageTemp = "PRIVMSG #" + self.CHANNEL + " :" + message
            self.irc.send((messageTemp + "\n").encode())


    def decodeString(self,partStr):
        
        try:
            x = str(partStr[0:1])
            y = int(partStr[1:2])
            if y<8:
                
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
            print(self.guiOutput['decodeString'])
            self.message=""
            
      
    def get_text(self, lvl) -> str:

        if lvl:
            screenshot = ImageGrab.grab(bbox=(400,880,450,910))
            screenshot = screenshot.crop((5,10,40,25))
        else:
            screenshot = ImageGrab.grab(bbox=(870,880,905,910))
        scale = 4
        (width, height) = (screenshot.width * scale, screenshot.height * scale)
        screenshot = screenshot.resize((width, height))
        image = np.array(screenshot)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresholding = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        tessdata_dir_config = '--psm 7 -c tessedit_char_whitelist=0123456789/ --tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
        text = pytesseract.image_to_string(thresholding, config=tessdata_dir_config).strip()
        return text

    def get_text_gold(self) -> str:
        #print('ja gold')
        screenshot = ImageGrab.grab(bbox=(870,880,905,910))
        scale = 4
        (width, height) = (screenshot.width * scale, screenshot.height * scale)
        screenshot = screenshot.resize((width, height))
        image = np.array(screenshot)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grayscale,(5,5),0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        tessdata_dir_config = '--psm 7 -c tessedit_char_whitelist=0123456789/ --tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
        cv2.imwrite('gold.png', thresh)
        text = pytesseract.image_to_string(thresh, config=tessdata_dir_config).strip()
        return text 
  
    def adthresholding(self, image):
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 11)
    
    def findMatches(self, img, tmp, threshold=0.5) -> list:
        template = cv2.imread(tmp, 0)
        w, h = template.shape[::-1]
        template = self.adthresholding(template)
        res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where( res >= threshold)
        return list(zip(*loc[::-1]))
    
    
    def not_satisfy2(self, a,k,critical) -> bool:
        flag=False
        cx2,cy2 = k
        for i in a:
            cx1,cy1 = i
            if(abs(cx1-cx2) < critical and abs(cy1-cy2) < critical):
                flag=True
                break
        return flag
    
    def edit_list(self, a,length_of_a,critical) -> list:
        l = []
        l.append(a[0])
        i=1
        while(i < length_of_a):
            if(self.not_satisfy2(l,a[i],critical)==True):
                i+=1
            else:
                l.append(a[i])
                i+=1
        
        return l

    def get_items(self) -> list:
        screenshot = ImageGrab.grab()
        coord = (500,200,1375,725)
        screenshot = screenshot.crop(coord)
        image = np.array(screenshot)
        grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        width = int(grayscale.shape[1])
        height = int(grayscale.shape[0])
        dim = (width, height)
        resized = cv2.resize(grayscale, dim, interpolation = cv2.INTER_AREA)
        thresh = self.adthresholding(resized)
        cv2.imwrite('../output/res.png', thresh)
        
        ### White Items
        matches_w = self.findMatches(thresh, '../images/white.png')
        ###Blue Items
        matches_b = self.findMatches(thresh, '../images/blue.png')
        
        matches = []
        matches.extend(matches_w)
        matches.extend(matches_b)
        
        len_matches = len(matches)
        if len_matches > 0:
            loc = self.edit_list(matches, len_matches, 10)
        else:
            return None
        
        
        offset = 30
        omatches = []
        
        for pt in loc:
            omatches.append((pt[0]+coord[0]+offset,pt[1]+coord[1]+offset))
        if len(omatches) > 5:
            omatches = omatches[:4]
        
        return omatches
    
    
    def clickItems(self, locations):
        for loc in locations:
            pyautogui.click(loc[0],loc[1], button='right')
            pyautogui.mouseUp(button='right')
            time.sleep(3)
        pyautogui.click(470,650, button='right')
        pyautogui.mouseUp(button='right')
        self.clickIn()
    
    def clickIn(self):
        pyautogui.click(960,250, button='left')
        pyautogui.mouseUp(button='left')


    def addMessage(self, message):
        self.messagelist.append(self.message)
        print(self.messagelist)
                 
        if collections.Counter(self.messagelist)[message] == self.counter: #zählt die anzahl der aktuellen message in der vorhandenen messagelist
            self.rein = True
            self.voll = True
            
        else:
            self.message=""

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
        
        if("End of /NAMES list" in line):
            print(self.guiOutput['loadingComplete'] + self.CHANNEL + "' Channel!")
            return False
        else:
            return True

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

    def console(self, line) -> bool:
        
        if "PRIVMSG" in line:
            return False
        else:
            return True



    def gamecontrol(self, message=''):
        
        self.message = message.lower()

#UNITS KAUFEN
            
        if self.message.startswith('shop') and self.message[-1].isdigit() and len(self.message)<6 and 0< int(self.message[-1])<6:
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                z = int(self.message[4:])
                z = z - 1
                pyautogui.click(self.shoplist[z], button='left')
                pyautogui.mouseUp(button='left')
                self.resetVars()
    

        
#AUGMENT AUSWAHL
            
        elif self.message.startswith('aug') and self.message[-1].isdigit() and len(self.message)<5 and 0< int(self.message[-1])<4:
                
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                tempAug = int(self.message[3])
                pyautogui.click(self.augmentlist[tempAug-1])
                pyautogui.mouseUp(button='left')
                self.resetVars()


#LOCK/UNLOCK SHOP

        elif (self.message == 'lock') or (self.message == 'unlock'):
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                pyautogui.click(1450,900, button='left')
                pyautogui.mouseUp(button='left')
                self.resetVars()
            
#LOSLAUFEN KARUSSELL

        elif "now" == self.message:
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                pyautogui.click(950,370, button='right')
                pyautogui.mouseUp(button='right')
                self.resetVars()

#IITEMS EINSAMMELN

        elif self.message == 'collect':
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                items = self.get_items()
                print('Items:', items)
                
                if items is not None:
                    t2 = threading.Thread(target = self.clickItems, args=(items,))
                    t2.start()
                
                self.resetVars()

#REFRESH STORE

        elif (self.message =='lvl') or (self.message == 'lvlup'):
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                level = self.get_text(True)
                gold = self.get_text(False)

                print('Gold:', gold)
                print('Level:', level)
                    
                if gold.isdecimal():
                    gold = int(gold)

                
                    level = level.split('/')
                    if len(level) == 2:
                        a = level[0]
                        if a.isdecimal():
                            a = int(a)
                            b = level[1]
                            if b.isdecimal():
                                if self.message == 'lvl':
                                    b = int(b) - 2
                                else:
                                    b = int(b)
                                c = b - a
                                if c < 0:
                                    c = c + 30
                                clicks = c // 4 + (c % 4 > 0)
                        
                                print(str(a) + ' von ' + str(b) + ' XP, Kosten: ' + str(clicks*4) + ' Gold')
                                pyautogui.moveTo(375,960)
                                i = 0
                                if clicks*4 <= gold:
                                    
                                    while i < clicks:
                                        pyautogui.mouseDown(button="left")
                                        pyautogui.mouseUp(button="left")
                                        i += 1
                                        print(i)

                self.clickIn()            
                self.resetVars()

#ERFAHRUNG KAUFEN

        elif self.message == 'roll' or self.message == 'reroll':
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                pyautogui.click(375,1045)
                pyautogui.mouseUp(button="left")
                self.clickIn()
                self.resetVars()

#VERKAUFEN
            
        elif self.message.startswith('sellw') and len(self.message)<7 and self.message[4:5] in self.farblist and self.message[-1].isdigit() and int(self.message[-1])>0:
            
            if self.message[4:6] == "w8" or self.message[4:6] == "w9"or 0< int(self.message[-1]) <8:
                
                if not self.rein and not self.chaos:
                    self.addMessage(self.message)
                else:
                    self.clickIn()
                    z = self.decodeString(self.message[4:6])
                    pyautogui.moveTo(z)
                    pyautogui.mouseDown(button='left')
                    pyautogui.moveTo(self.shoplist[2])
                    pyautogui.mouseUp(button='left')
                    pyautogui.moveTo(z)
                    self.resetVars()
                    
#UNITS PLATZIEREN
            
#von Bank auf Felde
    
        elif len(self.message)<5 and self.message[0:1] in self.farblist and self.message[1:2].isnumeric() and self.message[2:3] in self.farblist and self.message[3:4].isnumeric():
            
            if (self.message[2:4] == "w8" or self.message[2:4] == "w9" or 1 <= int(self.message[-1]) <=7) and (self.message[0:2] == "w8" or self.message[0:2] == "w9" or 1<= int(self.message[1:2]) <=7):
                
                if not self.rein and not self.chaos:
                    self.addMessage(self.message)
                else:
                    self.clickIn()
                    origin = str(self.message[0:2])
                    aim = str(self.message[2:4]) 
                    pyautogui.moveTo(self.decodeString(origin))
                    pyautogui.mouseDown(button='left')
                    pyautogui.moveTo(self.decodeString(aim))
                    pyautogui.mouseUp(button='left')
                    self.resetVars()  


#ITEMS EINSAMMELN                       
        elif self.message.startswith('row') and len(self.message)<5 and self.message[-1].isdigit() and 0< int(self.message[-1]) <9:
            
            if not self.rein and not self.chaos:
                self.addMessage(self.message)
            else:
                self.clickIn()
                z = int(self.message[3:])
                temp = ((self.Rowlist[z])[0][0] - 100, (self.Rowlist[z])[0][1])
                pyautogui.click(temp,button='right')
                pyautogui.mouseUp(button='right')
                time.sleep(2)
                temp = ((self.Rowlist[z])[6][0] + 100, (self.Rowlist[z])[6][1])
                print(temp, type(temp))
                pyautogui.click(temp,button='right')
                pyautogui.mouseUp(button='right')
                self.resetVars()

#ITEMS VERTEILEN
        elif self.message[0:1] in self.itemWhitelist and self.message[1:2] in self.farblist and len(self.message)<4 and self.message[-1].isdigit():
            
            if self.message[1:3] == "w8" or self.message[1:3] == "w9" or 0< int(self.message[-1]) <8:
                
                if not self.rein and not self.chaos:
                    self.addMessage(self.message)
                else:
                    self.clickIn()
                    slot = str(self.message[0:1])
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
                    pyautogui.moveTo(self.decodeString(self.message[1:]))
                    pyautogui.mouseUp(button='left')
                    self.resetVars()
        

        
        if self.voll and not self.chaos:
            if self.message != self.old_message:
                print(self.guiOutput['foundCommand'], self.message)
                self.rein = True
                self.voll = False
                self.messagelist.clear()
                self.old_message = self.message
                self.gamecontrol(self.message)
            else:
                print(self.guiOutput['commandWontRepeat'])
                self.messagelist = list(filter((self.message).__ne__, self.messagelist))
                print(self.messagelist)
                self.resetVars()
                
                    
    def start_bot(self):
        self.stop_thread.clear()
        self.thread = threading.Thread(target=self.twitch)
        self.thread.start()
    

    def stop(self):
        self.stop_thread.set()
        self.thread.join()
        self.thread = None
    
    def twitch(self):
        global foo
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
