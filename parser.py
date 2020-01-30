import actions
import state
import cards
import random

def a(n):
    non_starters = [a for a in actions.available_actions if not a['starter']]
    if non_starters and len(non_starters > 1):
        n = random.randrange(0, len(non_starters))
        for a in range(0, len(actions.available_actions)):
            if actions.available_actions[a] == non_starters[n]:
                actions.available_actions[a]['locked'] = n


def A(n):
    if cards.projects[n][3] is None:

        for a in range(0, len(actions.available_actions)):
            if actions.available_actions[a]['locked'] == n:
                actions.available_actions[a]['locked'] = False
        return True
    actions.add_action(cards.projects[n][3])


def K(n):
    pass

s = lambda n: state.bump_track('S', -1)
S = lambda n: state.bump_track('S', 1)
n = lambda n: state.bump_track('N', -1)
N = lambda n: state.bump_track('N', 1)
h = lambda n: state.bump_track('H', -1)
H = lambda n: state.bump_track('H', 1)

C = lambda n: state.gain('C', 1)
U = lambda n: state.gain('U', 1)
R = lambda n: state.gain('R', 1)
c = lambda n: state.gain('C', -1)
u = lambda n: state.gain('U', -1)
r = lambda n: state.gain('R', -1)

T = lambda n: state.add_threat(cards.threats[n])
t = lambda n: state.remove_threat()
P = lambda n: state.add_project(cards.projects[n])
p = lambda n: state.remove_project()
G = lambda n: actions._upgrade()
M = lambda n: state.accelerate_threat()

def Z(n):
    if state.RESOURCES['R'] >= 3:
        actions.finish(win=True)
    if state.RESOURCES['C'] == 0:
        actions.finish(win=False)
    state.gain("C", -1)

def Y(n):
    if state.TRACKS['S'] >=2:
        actions.finish(win=True)
    if state.TRACKS['S'] <= -2:
        actions.finish(win=False)

def X(n):
    if state.TRACKS['H'] >=2:
        actions.finish(win=True)
    if state.TRACKS['H'] <= -2:
        actions.finish(win=False)

def W(n):
    if state.TRACKS['N'] >=2:
        actions.finish(win=True)
    if state.TRACKS['N'] <= -2:
        actions.finish(win=False)