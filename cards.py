import state
import actions
import random
import parser


def execute(card, tries=0):
    if tries > 5:
        return False

    number, effect = card
    option = random.choice(effect)

    state.begin()
    for l in option:
        success = getattr(parser, l)(number)
        if(len(effect) > 1 and not success):
            state.rollback()
            return execute(card, tries+1)


"""
s/h/n = lose a Security/Health/Unity
S/H/N = Gain a Security/Health/Unity
c/u/r = Lose a common/uncommon/rare
C/U/R = Gain a common/uncommon/rare
T = add the associated threat
t = lose a threat
a = lose a random (non-starter) action
A = Gain the action lost again
P = add the associated project
p = lose a random project
K = skip a worker placement
M = Move threats to the right
G = Upgrade an action
"""
cards = {
    "threats": {
        6: ['sT'],
        7: ['hT'],
        8: ['nT'],
        9: ['sT'],
        10: ['hT'],
        11: ['uT'],
        12: ['uu', 's'],
        13: ['cccc', 'n'],
        14: ['T', 'uu'],
        15: ['aP'],
        16: ['n'],
        17: ['n'],
        18: ['aP'],
        19: ['sccc', 'su'],
        20: ['uu', 'n'],
        21: ['Ts'],
        22: ['s','h','n'],
        23: ['T'],
        24: ['p'],
        25: ['ccc'],
        26: ['u'],
        27: ['aP'],
        28: ['s', 'n'],
        29: ['uu', 's'],
        30: ['n', 's'],
        31: ['h', 'u'],
        32: ['K'],
        33: ['KM'],
        34: ['sT'],
        35: ['hT'],
        36: ['nT'],
        37: ['p'],
        38: ['hT'],
        39: ['n'],
        40: ['KM'],
        41: ['cccT'],
        42: ['KM']
    },
    # 43: Make a threat cost R
    "boons": {
        44: ['UP'],
        45: ['P'],
        46: ['P'],
        47: ['P'],
        48: ['UUP'],
        49: ['P'],
        50: ['P'],
        51: ['P'],
        52: ['P'],
        53: ['SSu','s'],
        54: ['SSh','s'],
        55: ['HHs','h'],
        56: ['HHu','h'],
        57: ['NNs','n'],
        58: ['NNh','n'],
        59: ['cccR', ''],
        60: ['Ru', 'Rs'],
        61: ['U'],
        62: ['t'],
        63: ['sN', 'sH', 'sUU', ''],
        64: ['N'],
        65: ['c'],
        66: ['Pu'],
        67: ['P'],
    }
}

threats = {
    6: (6, 'cccccc', 'S', 's'),
    7: (7, 'cccccc', 'H', 'h'),
    8: (8, 'cccccc', 'N', 'n'),
    9: (9, 'uu', 'S', 'cs'),
    10: (10, 'uu', 'H', 'ch'),
    11: (11, 'uu', 'N', 'cn'),
    14: (14, 'uu', 'N', 'hhc'),
    21: (21, 'r', 'SS', 's'),
    23: (23, 'ccccc', 'NN', 'n'),
    34: (34, 'uuu', 'S', 's'),
    35: (35, 'uuu', 'H', 'h'),
    36: (36, 'uuu', 'N', 'n'),
    38: (38, 'uuu', 'H', 'h'),
    41: (41, 'u', 'C', 'c'),
}
projects = {
    15: (15, 'ccccu', 'A', None),
    18: (18, 'cccc', 'A', None),
    27: (27, 'ccu', 'A', None),
    44: (44, 'cccc', 'A', actions.filter),
    45: (45, 'ucc', 'AS', actions.bump_sec),
    46: (46, 'ucc', 'AH', actions.bump_hp),
    47: (47, 'ucc', 'UA', actions.bump_un),
    48: (48, 'ccccc', 'UA', actions.gain_uc),
    49: (49, 'ccc', 'SA', actions.switch_threat),
    50: (50, 'ccc', 'G'),
    51: (51, 'ccc', 'UA', actions.reuse),
    52: (52, 'uuu', 'R'),
    66: (66, 'uuu', 'NN'),
    67: (67, 'uuu', 'R'),
}

endings = {
    68: 'Z',
    69: 'Y',
    70: 'X',
    71: 'W',
    72: "NM",
    73: "HM",
    74: "SM",
    75: ['SM', 'HM', 'NM']
}