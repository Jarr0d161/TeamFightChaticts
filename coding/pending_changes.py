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
import json
from dataclasses import dataclass, field
from typing import List, Tuple

import pandas as pd
from TFTScreenGrabber import get_level_text, get_gold_text


@dataclass
class TwitchBotConfig:
    config_filepath: str='config/ui_augments.json'
    self.reihe1: List[Tuple[int, int]]=field(init=False)
    self.reihe2: List[Tuple[int, int]]=field(init=False)
    self.reihe3: List[Tuple[int, int]]=field(init=False)
    self.reihe4: List[Tuple[int, int]]=field(init=False)
    self.reihe5: List[Tuple[int, int]]=field(init=False)
    self.reihe6: List[Tuple[int, int]]=field(init=False)
    self.reihe7: List[Tuple[int, int]]=field(init=False)
    self.reihe8: List[Tuple[int, int]]=field(init=False)
    self.banklist: List[Tuple[int, int]]=field(init=False)
    self.augmentlist: List[Tuple[int, int]]=field(init=False)
    self.itemlist: List[Tuple[int, int]]=field(init=False)
    self.shoplist: List[Tuple[int, int]]=field(init=False)
    self.comlist: List[Tuple[int, int]]=field(init=False)
    self.farblist: List[str]=field(init=False)
    self.itemWhitelist: List[str]=field(init=False)

    def __post_init__(self):
        with open(config_filepath, 'r') as file:
            config = json.load(file)

        self.reihe1 = config['reihe1']
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

    @property
    def Rowlist(self) -> List[List[Tuple[int, int]]]:
        return [self.banklist, self.reihe1, self.reihe2, self.reihe3, self.reihe4,
                self.reihe5, self.reihe6, self.reihe7, self.reihe8]


@dataclass
class TwitchConnection:
    SERVER: str = "irc.twitch.tv"
    PORT: int = 6667
    BOT: str = "TeamFightChaticts"
    PASS: str = self.confList.loc['auth'][0]
    CHANNEL: str = self.confList.loc['channel'][0]
    OWNER: str = self.confList.loc['channel'][0]