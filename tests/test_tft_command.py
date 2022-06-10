from teamfightchaticts.tft_command import TFTCommand, TFTCmdType


# TFTCmdType.SHOP: '^shop[1-5]$',
def test_can_parse_shop_unit_cmd():
    match_cmd = lambda cmd, cmd_type, unit: \
        cmd.cmd_type == cmd_type \
            and cmd.selected_shop_unit == unit
    assert match_cmd(TFTCommand('shop1'), TFTCmdType.SHOP, 0)
    assert match_cmd(TFTCommand('shop2'), TFTCmdType.SHOP, 1)
    assert match_cmd(TFTCommand('shop3'), TFTCmdType.SHOP, 2)
    assert match_cmd(TFTCommand('shop4'), TFTCmdType.SHOP, 3)
    assert match_cmd(TFTCommand('shop5'), TFTCmdType.SHOP, 4)
    assert match_cmd(TFTCommand('shop0'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('shop6'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('shop10'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand(' shop1'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('shop1 '), TFTCmdType.INVALID, None)


# TFTCmdType.PICK_AUGMENT: '^aug[1-3]$',
def test_can_parse_pick_augment_cmd():
    match_cmd = lambda cmd, cmd_type, aug: \
        cmd.cmd_type == cmd_type \
            and cmd.selected_augment == aug
    assert match_cmd(TFTCommand('aug1'), TFTCmdType.PICK_AUGMENT, 0)
    assert match_cmd(TFTCommand('aug2'), TFTCmdType.PICK_AUGMENT, 1)
    assert match_cmd(TFTCommand('aug3'), TFTCmdType.PICK_AUGMENT, 2)
    assert match_cmd(TFTCommand('aug0'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('aug4'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('aug10'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand(' aug1'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('aug1 '), TFTCmdType.INVALID, None)


# TFTCmdType.LOCK_OR_UNLOCK: '^(lock|unlock)$',
def test_can_parse_lock_or_unlock_cmd():
    assert TFTCommand('lock').cmd_type == TFTCmdType.LOCK_OR_UNLOCK
    assert TFTCommand('unlock').cmd_type == TFTCmdType.LOCK_OR_UNLOCK
    assert TFTCommand(' lock').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lock ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' unlock').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('unlock ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.PICK_ITEM_CAROUSEL: '^now$',
def test_can_parse_pick_item_carousel_cmd():
    assert TFTCommand('now').cmd_type == TFTCmdType.PICK_ITEM_CAROUSEL
    assert TFTCommand(' now').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('now ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.COLLECT_ALL_ITEMS_DROPPED: '^collect$',
def test_can_parse_collect_items_dropped_cmd():
    assert TFTCommand('collect').cmd_type == TFTCmdType.COLLECT_ALL_ITEMS_DROPPED
    assert TFTCommand(' collect').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('collect ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.LEVELUP: '^(lvl|lvlup)$',
def test_can_parse_levelup_cmd():
    assert TFTCommand('lvl').cmd_type == TFTCmdType.LEVELUP
    assert TFTCommand('lvlup').cmd_type == TFTCmdType.LEVELUP
    assert TFTCommand(' lvl').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lvl ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' lvlup').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lvlup ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.ROLL_SHOP: '^(roll|reroll)$',
def test_can_parse_roll_shop_cmd():
    assert TFTCommand('roll').cmd_type == TFTCmdType.ROLL_SHOP
    assert TFTCommand('reroll').cmd_type == TFTCmdType.ROLL_SHOP
    assert TFTCommand(' roll').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('roll ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' reroll').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('reroll ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.SELL_UNIT: '^sellw[0-9]$',
def test_can_parse_sell_bench_unit_cmd():
    match_cmd = lambda cmd, cmd_type, unit: \
        cmd.cmd_type == cmd_type \
            and cmd.unit_to_sell == unit
    assert match_cmd(TFTCommand('sellw0'), TFTCmdType.SELL_UNIT, 'w0')
    assert match_cmd(TFTCommand('sellw1'), TFTCmdType.SELL_UNIT, 'w1')
    assert match_cmd(TFTCommand('sellw2'), TFTCmdType.SELL_UNIT, 'w2')
    assert match_cmd(TFTCommand('sellw3'), TFTCmdType.SELL_UNIT, 'w3')
    assert match_cmd(TFTCommand('sellw4'), TFTCmdType.SELL_UNIT, 'w4')
    assert match_cmd(TFTCommand('sellw5'), TFTCmdType.SELL_UNIT, 'w5')
    assert match_cmd(TFTCommand('sellw6'), TFTCmdType.SELL_UNIT, 'w6')
    assert match_cmd(TFTCommand('sellw7'), TFTCmdType.SELL_UNIT, 'w7')
    assert match_cmd(TFTCommand('sellw8'), TFTCmdType.SELL_UNIT, 'w8')
    assert match_cmd(TFTCommand('sellw9'), TFTCmdType.SELL_UNIT, 'w9')
    assert match_cmd(TFTCommand(' sellw0'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('sellw0 '), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('sellw'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('sellwx'), TFTCmdType.INVALID, None)


# TFTCmdType.PLACE_UNIT: '^(w[0-9]|[lbgr][1-7]){2}$',
def test_can_parse_place_unit_cmd():
    match_cmd = lambda cmd, cmd_type, unit, aim: \
        cmd.cmd_type == cmd_type \
            and cmd.unit_to_place == unit \
            and cmd.unit_place_aim == aim

    bench = [f'w{i}' for i in range(10)]
    board = [f'{row}{i}' for row in ['l', 'b', 'g', 'r'] for i in range(1, 8)]
    all_fields = bench + board
    valid_perms = [(f1, f2) for f1 in all_fields for f2 in all_fields if f1 != f2]
    invalid_perms = [(f1, f1) for f1 in all_fields]

    assert all(map(lambda perm: match_cmd(
        TFTCommand(f'{perm[0]}{perm[1]}'), TFTCmdType.PLACE_UNIT, perm[0], perm[1]), valid_perms))
    assert all(map(lambda perm: match_cmd(
        TFTCommand(f'{perm[0]}{perm[1]}'), TFTCmdType.INVALID, None, None), invalid_perms))

    assert match_cmd(TFTCommand('a0a1'), TFTCmdType.INVALID, None, None)
    assert match_cmd(TFTCommand(' w0w1'), TFTCmdType.INVALID, None, None)
    assert match_cmd(TFTCommand('w0w1 '), TFTCmdType.INVALID, None, None)


# TFTCmdType.COLLECT_ITEMS_OF_ROW: '^row[1-8]$',
def test_can_parse_collect_items_of_row_cmd():
    match_cmd = lambda cmd, cmd_type, row: \
        cmd.cmd_type == cmd_type \
            and cmd.row_to_collect == row
    
    # TFTCmdType.COLLECT_ITEMS_OF_ROW
    assert match_cmd(TFTCommand('row1'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 1)
    assert match_cmd(TFTCommand('row2'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 2)
    assert match_cmd(TFTCommand('row3'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 3)
    assert match_cmd(TFTCommand('row4'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 4)
    assert match_cmd(TFTCommand('row5'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 5)
    assert match_cmd(TFTCommand('row6'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 6)
    assert match_cmd(TFTCommand('row7'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 7)
    assert match_cmd(TFTCommand('row8'), TFTCmdType.COLLECT_ITEMS_OF_ROW, 8)
    assert match_cmd(TFTCommand('row0'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('row9'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand(' row1'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('row1 '), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('row'), TFTCmdType.INVALID, None)
    assert match_cmd(TFTCommand('rowx'), TFTCmdType.INVALID, None)

# TFTCmdType.ATTACH_ITEM: '^[a-j](w[0-9]|[lbgr][1-7])$',
def test_can_parse_attach_item_to_unit_cmd():
    match_cmd = lambda cmd, cmd_type, item, unit: \
        cmd.cmd_type == cmd_type \
            and cmd.item_to_atttach == item \
            and cmd.unit_to_attach_to == unit

    bench = [f'w{i}' for i in range(10)]
    board = [f'{row}{i}' for row in ['l', 'b', 'g', 'r'] for i in range(1, 8)]
    all_fields = bench + board
    item_slots = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    valid_perms = [(item, unit) for item in item_slots for unit in all_fields]

    assert all(map(lambda perm: match_cmd(
        TFTCommand(f'{perm[0]}{perm[1]}'), TFTCmdType.ATTACH_ITEM,
                   perm[0].encode()[0] - 'a'.encode()[0], perm[1]), valid_perms))

    assert match_cmd(TFTCommand('ia1'), TFTCmdType.INVALID, None, None)
    assert match_cmd(TFTCommand(' iw1'), TFTCmdType.INVALID, None, None)
    assert match_cmd(TFTCommand('iw1 '), TFTCmdType.INVALID, None, None)
