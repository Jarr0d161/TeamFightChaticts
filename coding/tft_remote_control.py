from typing import Tuple
import pyautogui


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
    pass
