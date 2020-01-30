import state
import parser
import random

U = 'U'
C = 'C'
R = 'R'

available_actions = []

def workers_as_string():
    return " ".join(["{}:{}".format(a['action'].__name__, a['workers']) for a in available_actions if a['workers'] > 0])


def add_action(method, upgraded=False, multi_use=False, starter=True):
    available_actions.append({
        "workers": 0,
        "upgraded": upgraded,
        "action": method,
        "multi_use": multi_use,
        "starter": starter,
        "locked": False
    })


def take_random_action(currently_on, tries=0):
    n, action = random_action()
    if not action['action'](action['upgraded']):
        return take_random_action(currently_on, tries+1)

    move_worker(currently_on, to=n)
    return n, action


def random_action():
    n = random.randrange(0, len(available_actions))
    action = available_actions[n]

    if action['locked']:
        print "Locked action ", action['action']
        return random_action()

    if action['workers'] == 0 or action['multi_use']:
        return n, action
    return random_action()


def move_worker(_from, to):
    available_actions[to]['workers'] += 1
    if _from >= 0:
        available_actions[_from]['workers'] -= 1


def _do_card(_list, tries=0):
    active = len(_list)
    if tries > 5 or active == 0:
        return False
    n = random.randrange(0, active)
    p = _list[n]

    state.begin()
    for l in p[1]:
        if not getattr(parser, l)(p[0]):
            state.rollback()
            if active == 1:
                return False
            return _do_card(_list, tries + 1)

    for l in p[2]:
        getattr(parser, l)(p[0])
    return n


def project(upgraded, tries=0):
    n = _do_card(state.PROJECTS)
    if n is False:
        return False
    state.remove_project(n)
    return True


def threat(upgraded, tries=0):
    n = _do_card(state.THREATS)
    if n is False:
        return False
    state.remove_threat(n)
    return True


def _upgrade(tries=0):
    if tries >= 5:
        return False

    n = random.randrange(0, len(available_actions))
    a = available_actions[n]
    if a['upgraded']:
        return _upgrade(tries+1)
    available_actions[n]['upgraded'] = True
    return True


def upgrade(upgraded):
    if not state.can_afford(U, 2):
        return False
    did_upgrade = _upgrade()
    if did_upgrade:
        state.gain(U, -2)
    return did_upgrade


def gain_c(upgraded):
    return state.gain(C, (2 if upgraded else 1))


def filter(upgraded):
    if not state.can_afford(C, 1):
        return False
    state.gain(C, -1)
    state.gain(U, (2 if upgraded else 1))
    return True


def bump_sec(upgraded):
    if not state.can_afford(U, 1 if upgraded else 2):
        return False
    state.bump_track('S', 1)
    return True


def bump_un(upgraded):
    if not state.can_afford(U, 1 if upgraded else 2):
        return False
    state.bump_track('H', 1)
    return True


def bump_hp(upgraded):
    if not state.can_afford(U, 1 if upgraded else 2):
        return False
    state.bump_track('S', 1)
    return True


def switch_threat(upgraded):
    if not state.can_afford(U, 1 if upgraded else 2):
        return False
    # We're picking randomly, so this doesn't actually need to be implemented


def gain_uc(upgraded):
    state.gain('U', 1)
    if upgraded:
        state.gain('C', 1)


def reuse(upgraded, tries=0):
    if tries > 5:
        return False
    def get_used_action():
        n = random.randrange(0, len(available_actions))
        action = available_actions[n]

        if action['workers'] > 0:
            return n, action
        return get_used_action()

    n, action = get_used_action()
    if not action['action'](action['upgraded']):
        return reuse(upgraded, tries + 1)

    return True


def finish(win):
    w = "WIN " if win else "LOSE"
    if win is None:
        w = "FAIL"
    print "*"*41
    print "*\t\tYOU {}\t\t*".format(w)
    print "*"*41
    exit()