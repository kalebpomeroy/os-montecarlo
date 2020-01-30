import random
import cards
import state
import actions
from itertools import cycle

turns = 0
total_cards = 28
player_workers = [-1, -1, -1, -1]


def take_action(p):
    n, action = actions.take_random_action(player_workers[p])
    player_workers[p] = n

    return action['action'].__name__


actions.add_action(actions.gain_c, multi_use=True, starter=True)
actions.add_action(actions.upgrade, upgraded=True, starter=True)
actions.add_action(actions.project, upgraded=True, starter=True)
actions.add_action(actions.threat, upgraded=True, starter=True)
actions.add_action(actions.filter, starter=True)

# Build the deck, skipping the starting cards
boons = cards.cards['boons'].keys()
threats = cards.cards['threats'].keys()
endings = cards.endings.keys()
random.shuffle(boons)
random.shuffle(threats)
random.shuffle(endings)

main_deck = [(k, cards.cards['boons'][k]) for k in boons[:total_cards/2]] + [(k, cards.cards['threats'][k]) for k in threats[:total_cards/2]]
random.shuffle(main_deck)
deck = [(k, cards.endings[k]) for k in endings] + main_deck

for p in cycle([0, 1, 2, 3]):
    try:
        card = deck.pop()
        cards.execute(card)
    except IndexError:
        break
    action = take_action(p)
    print "P{} draw:{} action:{} \t{} \t{} \t{}".format(
        p+1,
        card[0],
        action,
        state.as_str(),
        actions.workers_as_string(),
        state.p_t_as_str())
    if (state.TRACKS['S'] <= -5 or state.TRACKS['H'] <= -5 or state.TRACKS['N'] <= -5):
        actions.finish(win=False)
