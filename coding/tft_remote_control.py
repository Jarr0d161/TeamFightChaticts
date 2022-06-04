import re
import time
import math
import threading
from typing import Tuple, List
import pyautogui

from .tft_screen_capture import capture_level, capture_gold, capture_item_locations


class MouseRemoteControl:
    @staticmethod
    def click_at(loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.mouseUp(button="left")

    @staticmethod
    def double_click_at(loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.mouseUp(button="left")
        pyautogui.mouseDown(button="left")
        pyautogui.mouseUp(button="left")

    @staticmethod
    def right_click_at(loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="right")
        pyautogui.mouseUp(button="right")

    @staticmethod
    def drag_item(x_start: int, y_start: int, x_end: int, y_end: int):
        pyautogui.moveTo(x_start, y_start)
        pyautogui.mouseDown(button="left")
        pyautogui.moveTo(x_end, y_end)
        pyautogui.mouseUp(button="left")


class TFTRemoteControl:
    def __init__(self):
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
        self.item_whitelist = ["a","b","c","d","e","f","g","h","i","j"]
        # TODO: don't put the Twitch commands here, this should be abstracted away ...

    def gamecontrol(self, message=''):
        if self.is_shop_cmd(message):
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

    def compute_item_drop_positions(self) -> list:
        OFFSET = 30
        SEARCH_BOX = (500, 200, 1375, 725)
        item_locs = capture_item_locations(SEARCH_BOX)
        if not item_locs:
            return None
        return [(p[0] + SEARCH_BOX[0] + OFFSET, p[1] + SEARCH_BOX[1] + OFFSET) for p in item_locs]

    def collect_dropped_items_at(self, locations: List[Tuple[int, int]]):
        # TODO: set this value to the units (in pixels) that can be walked by the avatar within a second
        LL_VELOCITY = 150
        LL_DEFAULT_POS = (470, 650)

        # TODO: use Dijkstra algorithm to compute the shortest path instead of randomly walking between items

        # walk towards first location
        locations.insert(0, LL_DEFAULT_POS)
        for pos_from, pos_to in zip(locations[:-1], locations[1:]):
            distance = math.dist(pos_from, pos_to)
            pyautogui.click(pos_to[0], pos_to[1], button='right')
            pyautogui.mouseUp(button='right')
            time.sleep(distance / LL_VELOCITY)

        pyautogui.click(LL_DEFAULT_POS[0], LL_DEFAULT_POS[1], button='right')
        pyautogui.mouseUp(button='right')
        self.click_in()

    def click_in(self):
        pyautogui.click(960, 250, button='left')
        pyautogui.mouseUp(button='left')

    def handle_shop_cmd(self, message: str):
        self.click_in()
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
        self.click_in()
        selected_augment = self.augmentlist[int(message[3])-1]
        pyautogui.click(selected_augment)
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_augment_cmd(self, message: str) -> bool:
        # TODO: use a regex to match the command, e.g. ^aug[1-3]$
        return message.startswith('aug') \
            and message[-1].isdigit() \
            and len(message) == 4 \
            and 0 < int(message[-1]) < 4

    def handle_lock_or_unlock_cmd(self, message: str):
        self.click_in()
        pyautogui.click(1450, 900, button='left')
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_lock_or_unlock_cmd(self, message: str) -> bool:
        return message in ['lock', 'unlock']

    def handle_karussell_cmd(self, message: str):
        self.click_in()
        pyautogui.click(950, 370, button='right')
        pyautogui.mouseUp(button='right')
        self.reset_vars()

    def is_karussell_cmd(self, message: str) -> bool:
        return message == "now"

    def handle_collect_cmd(self, message: str):
        self.click_in()
        items = self.compute_item_drop_positions()
        print('Items:', items)
        if items:
            # TODO: remove multithreading, this can lead to very weird behavior if the mouse is used for another command
            t2 = threading.Thread(target = self.collect_dropped_items_at, args=(items,))
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

        self.click_in()            
        self.reset_vars()

    def is_levelup_cmd(self, message: str) -> bool:
        return message in ['lvl', 'lvlup']

    def handle_roll_cmd(self, message: str):
        pyautogui.click(375,1045)
        pyautogui.mouseUp(button="left")
        self.click_in()
        self.reset_vars()

    def is_roll_cmd(self, message: str) -> bool:
        return message in ['roll', 'reroll']

    def handle_sellw_cmd(self, message: str):
        self.click_in()
        z = self.position_by_field_id(message[4:6])
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
            and (message[4:6] in ["w8", "w9"] or 0 < int(message[-1]) < 8)

    def handle_place_unit_cmd(self, message: str):
        self.click_in()
        origin = str(message[0:2])
        aim = str(message[2:4]) 
        pyautogui.moveTo(self.position_by_field_id(origin))
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(self.position_by_field_id(aim))
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_place_unit_cmd(self, message: str) -> bool:
        return len(message) < 5 and message[0:1] in self.farblist and message[1:2].isnumeric() \
            and message[2:3] in self.farblist and message[3:4].isnumeric() \
            and (message[2:4] == "w8" or message[2:4] == "w9" or 1 <= int(message[-1]) <= 7) \
            and (message[0:2] == "w8" or message[0:2] == "w9" or 1 <= int(message[1:2]) <= 7)

    def handle_collect_items_cmd(self, message: str):
        self.click_in()
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
        self.click_in()
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
        pyautogui.moveTo(self.position_by_field_id(message[1:]))
        pyautogui.mouseUp(button='left')
        self.reset_vars()

    def is_attach_item_cmd(self, message: str) -> bool:
        return message[0:1] in self.item_whitelist and message[1:2] in self.farblist \
            and len(message) < 4 and message[-1].isdigit() \
            and message[1:3] == "w8" or message[1:3] == "w9" or 0 < int(message[-1]) < 8

    def position_by_field_id(self, field_id: str) -> Tuple[int, int]:
        if len(field_id) != 2 or not field_id[0].isalpha() \
                or not field_id[1].isdecimal():
            return None

        row = field_id[0:1]
        col = int(field_id[1:2])

        if row.startswith('w'):
            return self.bench[col-1]

        if col >= 8:
            return None
        if row.startswith('l'):
            return self.row_1[col-1]
        if row.startswith('b'):
            return self.row_2[col-1]
        if row.startswith('g'):
            return self.row_3[col-1]
        if row.startswith('r'):
            return self.row_4[col-1]
