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
    cmd_patterns: Dict[TFTCmdType, str]=field(hash=False, compare=False,
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

    @property
    def type(self) -> TFTCmdType:
        for type in self.cmd_patterns:
            if re.match(self.cmd_patterns[type], self.cmd):
                return type
        return TFTCmdType.INVALID

    @property
    def selected_shop_unit(self) -> int:
        return int(self.cmd[4]) - 1

    @property
    def selected_augment(self) -> int:
        return int(self.cmd[3]) - 1

    @property
    def unit_to_sell(self) -> str:
        return self.cmd[4:6]

    @property
    def unit_to_place(self) -> str:
        return self.cmd[0:2]

    @property
    def unit_place_aim(self) -> str:
        return self.cmd[2:4]

    @property
    def row_to_collect(self) -> str:
        return int(self.cmd[3:])

    @property
    def item_to_atttach(self) -> int:
        slot_char = self.cmd[0].encode()[0]
        index = slot_char - "a".encode()[0]
        return index

    @property
    def unit_to_attach_to(self) -> str:
        return self.cmd[1:]
