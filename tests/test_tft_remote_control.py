from math import dist
from enum import IntEnum
from typing import Tuple, List
from dataclasses import dataclass, field

from teamfightchaticts.settings import AppSettings
from teamfightchaticts.tft_command import TFTCommand
from teamfightchaticts.tft_remote_control import \
    TFTRemoteControl, TFTRemoteControlPositions


@dataclass
class LevelupScreenCaptureMock:
    level: Tuple[int, int]
    gold: int

    def capture_level(self) -> Tuple[int, int]:
        return self.level

    def capture_gold(self) -> int:
        return self.gold

    def capture_item_locations(self, _: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        raise NotImplementedError()


@dataclass
class CollectItemsScreenCaptureMock:
    item_locations: List[Tuple[int, int]]

    def capture_level(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def capture_gold(self) -> int:
        raise NotImplementedError()

    def capture_item_locations(self, _: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        return self.item_locations


class NoScreenCaptureMock:
    def capture_level(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def capture_gold(self) -> int:
        raise NotImplementedError()

    def capture_item_locations(self, _: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        raise NotImplementedError()


class ClickType(IntEnum):
    LEFT_CLICK=0
    RIGHT_CLICK=1
    DRAG=2


@dataclass(eq=True)
class ClickAction:
    click_type: ClickType
    pos_1: Tuple[int, int]
    pos_2: Tuple[int, int]


@dataclass
class MouseControlLogger:
    click_history: List[ClickAction]=field(default_factory=list)

    def click_at(self, loc: Tuple[int, int]):
        self.click_history.append(ClickAction(ClickType.LEFT_CLICK, loc, None))

    def right_click_at(self, loc: Tuple[int, int]):
        self.click_history.append(ClickAction(ClickType.RIGHT_CLICK, loc, None))

    def drag(self, from_loc: Tuple[int, int], to_loc: Tuple[int, int]):
        self.click_history.append(ClickAction(ClickType.DRAG, from_loc, to_loc))


def get_screen_positions():
    settings = AppSettings()
    pos = settings.tft_overlay_positions()
    return TFTRemoteControlPositions(pos)


def test_should_click_lock_button():
    mouse_log = MouseControlLogger()
    remote = TFTRemoteControl(get_screen_positions(), NoScreenCaptureMock(), mouse_log)
    remote.execute_cmd(TFTCommand('lock'))
    valid_act = lambda a: a.click_type == ClickType.LEFT_CLICK and dist(a.pos_1, (1450, 900)) < 5
    assert any(map(valid_act, mouse_log.click_history))

# TODO: put at least one example per TFT command
