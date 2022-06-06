from typing import Tuple

import pyautogui
pyautogui.FAILSAFE = False


class MouseControl:
    # pylint: disable=no-self-use
    def click_at(self, loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.mouseUp(button="left")

    def right_click_at(self, loc: Tuple[int, int]):
        pyautogui.moveTo(loc[0], loc[1])
        pyautogui.mouseDown(button="right")
        pyautogui.mouseUp(button="right")

    def drag(self, from_loc: Tuple[int, int], to_loc: Tuple[int, int]):
        pyautogui.moveTo(from_loc[0], from_loc[1])
        pyautogui.mouseDown(button="left")
        pyautogui.moveTo(to_loc[0], to_loc[1])
        pyautogui.mouseUp(button="left")
