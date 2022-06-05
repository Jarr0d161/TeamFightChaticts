import time
import math
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Callable, Any, Protocol

from .tft_command import TFTCommand, TFTCmdType


class TFTScreenCapture(Protocol):
    def capture_level(self) -> Tuple[int, int]:
        ...

    def capture_gold(self) -> int:
        ...

    def capture_item_locations(self, crop: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        ...


class MouseControl(Protocol):
    def click_at(self, loc: Tuple[int, int]):
        ...

    def right_click_at(self, loc: Tuple[int, int]):
        ...

    def drag(self, from_loc: Tuple[int, int], to_loc: Tuple[int, int]):
        ...


class TFTRemoteControlPositions:
    # TODO: compute the positions as properties depending on the screen resolution
    def __init__(self, settings: Dict[str, Any]):
        self.row_1 = settings['row_1']
        self.row_2 = settings['row_2']
        self.row_3 = settings['row_3']
        self.row_4 = settings['row_4']
        self.row_5 = settings['row_5']
        self.row_6 = settings['row_6']
        self.row_7 = settings['row_7']
        self.row_8 = settings['row_8']
        self.bench = settings['row_8']
        self.augment_list = settings['augment_list']
        self.item_list = settings['item_list']
        self.shop_list = settings['shop_list']
        self.com_list = settings['com_list']
        self.avatar_default = settings['avatar_default']
        self.avatar_velocity = settings['avatar_velocity']
        self.levelup_button = settings['levelup_button']
        self.roll_button = settings['roll_button']
        self.carousel_aim = settings['carousel_aim']
        self.lock_button = settings['lock_button']
        self.item_drop_region = settings['item_drop_region']
        self.item_offset = settings['item_offset']
        self.default_click_pos = settings['default_click_pos']
        self.board_locations= [
            self.bench, self.row_1, self.row_2, self.row_3, self.row_4,
            self.row_5, self.row_6, self.row_7, self.row_8
        ]

    def by_field(self, field_id: str) -> Tuple[int, int]:
        row = field_id[0]
        col = int(field_id[1])

        if row.startswith('w'):
            return self.bench[col-1]
        if row.startswith('l'):
            return self.row_1[col-1]
        if row.startswith('b'):
            return self.row_2[col-1]
        if row.startswith('g'):
            return self.row_3[col-1]
        if row.startswith('r'):
            return self.row_4[col-1]


@dataclass
class TFTRemoteControl:
    positions: TFTRemoteControlPositions
    screen_capture: TFTScreenCapture
    mouse: MouseControl
    cmd_handlers: Dict[TFTCmdType, Callable[[TFTCommand]], None] = field(init=False)

    def __post_init__(self):
        self.cmd_handlers = {
            TFTCmdType.SHOP: self.handle_shop_cmd,
            TFTCmdType.PICK_AUGMENT: self.handle_augment_cmd,
            TFTCmdType.LOCK_OR_UNLOCK: self.handle_lock_or_unlock_cmd,
            TFTCmdType.PICK_ITEM_CAROUSEL: self.handle_carousel_cmd,
            TFTCmdType.COLLECT_ALL_ITEMS_DROPPED: self.handle_collect_cmd,
            TFTCmdType.LEVELUP: self.handle_levelup_cmd,
            TFTCmdType.ROLL_SHOP: self.handle_roll_cmd,
            TFTCmdType.SELL_UNIT: self.handle_sell_bench_unit_cmd,
            TFTCmdType.PLACE_UNIT: self.handle_place_unit_cmd,
            TFTCmdType.COLLECT_ITEMS_OF_ROW: self.handle_collect_row_cmd,
            TFTCmdType.ATTACH_ITEM: self.handle_attach_item_cmd,
        }

    def execute_cmd(self, tft_cmd: TFTCommand):
        if tft_cmd.type in self.cmd_handlers:
            self.cmd_handlers[tft_cmd.type](tft_cmd.cmd) # TODO: refactor to put whole command object

    def handle_shop_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        unit = tft_cmd.selected_shop_unit
        shop_pos = self.positions.shop_list[unit]
        self.mouse.click_at(shop_pos)

    def handle_augment_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        augment_pos = self.positions.augment_list[tft_cmd.selected_augment]
        self.mouse.click_at(augment_pos)

    def handle_lock_or_unlock_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        self.mouse.click_at(self.positions.lock_button)

    def handle_carousel_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        self.mouse.right_click_at(self.positions.carousel_aim)

    def handle_collect_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        items = self.compute_item_drop_positions()
        if items:
            self.collect_dropped_items_at(items)

    def compute_item_drop_positions(self) -> list:
        offset = self.positions.item_offset
        box = self.positions.item_drop_region
        item_locs = self.screen_capture.capture_item_locations(box)
        if not item_locs:
            return None
        return [(p[0] + box[0] + offset, p[1] + box[1] + offset) for p in item_locs]

    def collect_dropped_items_at(self, locations: List[Tuple[int, int]]):
        # TODO: use Dijkstra algorithm to compute the shortest path instead of randomly walking between items
        locations.insert(0, self.positions.avatar_default)
        locations.append(self.positions.avatar_default)

        for pos_from, pos_to in zip(locations[:-1], locations[1:]):
            distance = math.dist(pos_from, pos_to)
            self.mouse.right_click_at(pos_to)
            if pos_to != self.positions.avatar_default:
                time.sleep(distance / self.positions.avatar_velocity)

        self.mouse.click_at(self.positions.default_click_pos)

    def handle_levelup_cmd(self, tft_cmd: TFTCommand):
        level = self.screen_capture.capture_level()
        gold = self.screen_capture.capture_gold()
        if not gold or not level:
            return
        act_xp, total_xp = level

        xp_diff_to_level = total_xp - act_xp
        levelup_clicks = math.ceil(xp_diff_to_level / 4)
        levelup_clicks -= 1 if tft_cmd.cmd == 'lvl' and xp_diff_to_level % 4 <= 2 else 0

        while levelup_clicks > 0 and levelup_clicks * 4 <= gold:
            self.mouse.click_at(self.positions.levelup_button)
            levelup_clicks -= 1

        self.mouse.click_at(self.positions.default_click_pos)

    def handle_roll_cmd(self, _: TFTCommand):
        self.mouse.click_at(self.positions.roll_button)
        self.mouse.click_at(self.positions.default_click_pos)

    def handle_sell_bench_unit_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        unit_pos = self.positions.by_field(tft_cmd.unit_to_sell)
        self.mouse.drag(unit_pos, self.positions.shop_list[2])

    def handle_place_unit_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        origin_pos = self.positions.by_field(tft_cmd.unit_to_place)
        aim_pos = self.positions.by_field(tft_cmd.unit_place_aim)
        self.mouse.drag(origin_pos, aim_pos)

    def handle_collect_row_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        row = tft_cmd.row_to_collect
        start_pos = ((self.positions.board_locations[row])[0][0] - 100,
                     (self.positions.board_locations[row])[0][1])
        self.mouse.right_click_at(start_pos)
        time.sleep(2)
        end_pos = ((self.positions.board_locations[row])[6][0] + 100,
                   (self.positions.board_locations[row])[6][1])
        self.mouse.right_click_at(end_pos)

    def handle_attach_item_cmd(self, tft_cmd: TFTCommand):
        self.mouse.click_at(self.positions.default_click_pos)
        item_pos = self.positions.item_list[tft_cmd.item_to_atttach]
        unit_pos = self.positions.by_field(tft_cmd.unit_to_attach_to)
        self.mouse.drag(item_pos, unit_pos)
