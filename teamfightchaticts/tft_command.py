import re
from enum import IntEnum
from typing import Dict
from dataclasses import dataclass, field


class TFTCmdType(IntEnum):
    INVALID=0
    SHOP=1
    PICK_AUGMENT=2
    LOCK_OR_UNLOCK=3
    PICK_ITEM_CAROUSEL=4
    COLLECT_ALL_ITEMS_DROPPED=5
    LEVELUP=6
    ROLL_SHOP=7
    SELL_UNIT=8
    PLACE_UNIT=9
    COLLECT_ITEMS_OF_ROW=10
    ATTACH_ITEM=11


@dataclass(eq=True)
class TFTCommand:
    cmd: str
    cmd_patterns: Dict[TFTCmdType, str]=field(hash=False, compare=False, repr=False,
        default_factory=lambda: {
            TFTCmdType.SHOP: '^shop[1-5]$',
            TFTCmdType.PICK_AUGMENT: '^aug[1-3]$',
            TFTCmdType.LOCK_OR_UNLOCK: '^(lock|unlock)$',
            TFTCmdType.PICK_ITEM_CAROUSEL: '^now$',
            TFTCmdType.COLLECT_ALL_ITEMS_DROPPED: '^collect$',
            TFTCmdType.LEVELUP: '^(lvl|lvlup)$',
            TFTCmdType.ROLL_SHOP: '^(roll|reroll)$',
            TFTCmdType.SELL_UNIT: '^sellw[0-9]$',
            TFTCmdType.PLACE_UNIT: '^(w[0-9]|[lbgr][1-7]){2}$',
            TFTCmdType.COLLECT_ITEMS_OF_ROW: '^row[1-8]$',
            TFTCmdType.ATTACH_ITEM: '^[a-j]w[0-9]$',
        })
    cmd_type: TFTCmdType=field(init=False, default=None)
    selected_shop_unit: int=field(init=False, default=None)
    selected_augment: int=field(init=False, default=None)
    unit_to_sell: str=field(init=False, default=None)
    unit_to_place: str=field(init=False, default=None)
    unit_place_aim: str=field(init=False, default=None)
    row_to_collect: str=field(init=False, default=None)
    item_to_atttach: str=field(init=False, default=None)
    unit_to_attach_to: str=field(init=False, default=None)

    def __post_init__(self):
        # determine command type
        self.cmd = self.cmd.lower()
        self.cmd_type = TFTCmdType.INVALID
        for cmd_type_check in self.cmd_patterns:
            if re.match(self.cmd_patterns[cmd_type_check], self.cmd):
                self.cmd_type = cmd_type_check
                break

        # parse type-specific command parameters
        if self.cmd_type == TFTCmdType.SHOP:
            self.selected_shop_unit = int(self.cmd[4]) - 1
        if self.cmd_type == TFTCmdType.PICK_AUGMENT:
            self.selected_augment = int(self.cmd[3]) - 1
        if self.cmd_type == TFTCmdType.SELL_UNIT:
            self.unit_to_sell = self.cmd[4:6]
        if self.cmd_type == TFTCmdType.PLACE_UNIT:
            self.unit_to_place = self.cmd[0:2]
            self.unit_place_aim = self.cmd[2:4]
            if self.unit_to_place == self.unit_place_aim:
                self.cmd_type = TFTCmdType.INVALID
        if self.cmd_type == TFTCmdType.COLLECT_ITEMS_OF_ROW:
            self.row_to_collect = int(self.cmd[3:])
        if self.cmd_type == TFTCmdType.ATTACH_ITEM:
            self.item_to_atttach = self.cmd[0].encode()[0] - "a".encode()[0]
            self.unit_to_attach_to = self.cmd[1:]
