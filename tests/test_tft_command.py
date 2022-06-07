from teamfightchaticts.tft_command import TFTCommand, TFTCmdType


# TFTCmdType.SHOP: '^shop[1-5]$',
def test_shop_unit_cmd():
    assert TFTCommand('shop1').cmd_type == TFTCmdType.SHOP \
        and TFTCommand('shop1').selected_shop_unit == 0
    assert TFTCommand('shop2').cmd_type == TFTCmdType.SHOP \
        and TFTCommand('shop2').selected_shop_unit == 1
    assert TFTCommand('shop3').cmd_type == TFTCmdType.SHOP \
        and TFTCommand('shop3').selected_shop_unit == 2
    assert TFTCommand('shop4').cmd_type == TFTCmdType.SHOP \
        and TFTCommand('shop4').selected_shop_unit == 3
    assert TFTCommand('shop5').cmd_type == TFTCmdType.SHOP \
        and TFTCommand('shop5').selected_shop_unit == 4
    assert TFTCommand('shop0').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('shop6').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('shop10').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' shop1').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('shop1 ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.PICK_AUGMENT: '^aug[1-3]$',
def test_pick_augment_cmd():
    assert TFTCommand('aug1').cmd_type == TFTCmdType.PICK_AUGMENT \
        and TFTCommand('aug1').selected_augment == 0
    assert TFTCommand('aug2').cmd_type == TFTCmdType.PICK_AUGMENT \
        and TFTCommand('aug2').selected_augment == 1
    assert TFTCommand('aug3').cmd_type == TFTCmdType.PICK_AUGMENT \
        and TFTCommand('aug3').selected_augment == 2
    assert TFTCommand('aug0').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('aug4').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('aug10').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' aug1').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('aug1 ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.LOCK_OR_UNLOCK: '^(lock|unlock)$',
def test_lock_or_unlock_cmd():
    assert TFTCommand('lock').cmd_type == TFTCmdType.LOCK_OR_UNLOCK
    assert TFTCommand('unlock').cmd_type == TFTCmdType.LOCK_OR_UNLOCK
    assert TFTCommand(' lock').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lock ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' unlock').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('unlock ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.PICK_ITEM_CAROUSEL: '^now$',
def test_pick_item_carousel_cmd():
    assert TFTCommand('now').cmd_type == TFTCmdType.PICK_ITEM_CAROUSEL
    assert TFTCommand(' now').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('now ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.COLLECT_ALL_ITEMS_DROPPED: '^collect$',
def test_collect_items_dropped_cmd():
    assert TFTCommand('collect').cmd_type == TFTCmdType.COLLECT_ALL_ITEMS_DROPPED
    assert TFTCommand(' collect').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('collect ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.LEVELUP: '^(lvl|lvlup)$',
def test_levelup_cmd():
    assert TFTCommand('lvl').cmd_type == TFTCmdType.LEVELUP
    assert TFTCommand('lvlup').cmd_type == TFTCmdType.LEVELUP
    assert TFTCommand(' lvl').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lvl ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' lvlup').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('lvlup ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.ROLL_SHOP: '^(roll|reroll)$',
def test_roll_shop_cmd():
    assert TFTCommand('roll').cmd_type == TFTCmdType.ROLL_SHOP
    assert TFTCommand('reroll').cmd_type == TFTCmdType.ROLL_SHOP
    assert TFTCommand(' roll').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('roll ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand(' reroll').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('reroll ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.SELL_UNIT: '^sellw[0-9]$',
def test_sell_bench_unit_cmd():
    assert TFTCommand('sellw0').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw0').unit_to_sell == 'w0'
    assert TFTCommand('sellw1').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw1').unit_to_sell == 'w1'
    assert TFTCommand('sellw2').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw2').unit_to_sell == 'w2'
    assert TFTCommand('sellw3').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw3').unit_to_sell == 'w3'
    assert TFTCommand('sellw4').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw4').unit_to_sell == 'w4'
    assert TFTCommand('sellw5').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw5').unit_to_sell == 'w5'
    assert TFTCommand('sellw6').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw6').unit_to_sell == 'w6'
    assert TFTCommand('sellw7').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw7').unit_to_sell == 'w7'
    assert TFTCommand('sellw8').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw8').unit_to_sell == 'w8'
    assert TFTCommand('sellw9').cmd_type == TFTCmdType.SELL_UNIT \
        and TFTCommand('sellw9').unit_to_sell == 'w9'
    assert TFTCommand(' sellw0').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('sellw0 ').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('sellw').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('sellwx').cmd_type == TFTCmdType.INVALID


# TFTCmdType.PLACE_UNIT: '^(w[0-9]|[lbgr][1-7]){2}$',
def test_place_unit_cmd():
    valid_cmd = lambda cmd, unit, aim: cmd.cmd_type == TFTCmdType.PLACE_UNIT \
        and cmd.unit_to_place == unit and cmd.unit_place_aim == aim

    bench = [f'w{i}' for i in range(10)]
    board = [f'{row}{i}' for row in ['l', 'b', 'g', 'r'] for i in range(1, 8)]
    all_fields = bench + board
    valid_perms = [(f1, f2) for f1 in all_fields for f2 in all_fields if f1 != f2]
    invalid_perms = [(f1, f1) for f1 in all_fields]

    assert all(map(lambda perm: valid_cmd(
        TFTCommand(f'{perm[0]}{perm[1]}'), perm[0], perm[1]), valid_perms))
    assert all(map(lambda perm: not valid_cmd(
        TFTCommand(f'{perm[0]}{perm[1]}'), perm[0], perm[1]), invalid_perms))

    assert TFTCommand(' w0w1').cmd_type == TFTCmdType.INVALID
    assert TFTCommand('w0w1 ').cmd_type == TFTCmdType.INVALID


# TFTCmdType.COLLECT_ITEMS_OF_ROW: '^row[1-8]$',
# TFTCmdType.ATTACH_ITEM: '^[a-j]w[0-9]$',
