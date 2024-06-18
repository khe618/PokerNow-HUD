import pandas as pd
from collections import defaultdict
from os import listdir
from os.path import isfile, join

path_to_logs = "logs"
files = [f for f in listdir(path_to_logs) if isfile(join(path_to_logs, f))]
logs = []
for file in files:
    df = pd.read_csv(path_to_logs + "/" + file)
    logs += list(reversed(df["entry"]))


hands = []
in_hand = False
curr_hand = []

for log in logs:
    if log.startswith("-- ending"):
        in_hand = False
        hands.append(curr_hand)
        curr_hand = []
    if in_hand:
        curr_hand.append(log)
    if log.startswith("-- starting"):
        in_hand = True

actions = ["folds", "calls", "raises"]
threebet_actions = ["folds", "calls", "raises"]
flop_actions = ["bets", "checks", "folds", "calls", "raises"]


preflop = {}
threebets = {}
cbets = {}
can_3bet = defaultdict(int)


for hand in hands:
    preflop_actions = {}
    raise_count = 0
    three_bet_actions = {}
    cbet_actions = {}
    street = "preflop"
    first_raiser = ""
    preflop_raiser = ""
    has_cbet = False #will not consider cbet after a raise to the cbet
    possible_3bettors = set()
    for log in hand:
        if log.startswith("Flop"):
            street = "flop"
        if log.startswith("Turn"):
            street = "turn"
        if log.startswith("River"):
            street = "river"
        
        if street == "preflop":
            for action in actions:
                if action in log:
                    player = log[1:log.index(" @")].lower()
                    if raise_count == 1:
                        possible_3bettors.add(player)
                    if player not in preflop_actions:
                        preflop_actions[player] = action
                    if action == "raises":
                        preflop_raiser = player
                        raise_count += 1
                        if raise_count == 1:
                            first_raiser = player
                        if raise_count == 2:
                            three_bet_actions[player] = action
                    elif raise_count == 2 and player == first_raiser:
                        three_bet_actions[player] = action

        if street == "flop":
            for action in flop_actions:
                if action in log:
                    player = log[1:log.index(" @")].lower()
                    if player == preflop_raiser and (action == "bets" or action == "checks"):
                        cbet_actions[player] = action
                        if action == "bets":
                            has_cbet = True
                    elif has_cbet:
                        cbet_actions[player] = action
                        if action == "raises":
                            has_cbet = False
            
                    
    for player, action in preflop_actions.items():
        if player not in preflop:
            preflop[player] = {action: 0 for action in actions}
        preflop[player][action] += 1

    for player, action in three_bet_actions.items():
        if player not in threebets:
            threebets[player] = {action: 0 for action in actions}
        threebets[player][action] += 1

    for player, action in cbet_actions.items():
        if player not in cbets:
            cbets[player] = {action: 0 for action in flop_actions}
        cbets[player][action] += 1

    for player in possible_3bettors:
        can_3bet[player] += 1
    

stats = {}
for player, player_actions in preflop.items():
    num_hands = sum(player_actions.values())
    vpip = round(100 * (player_actions["calls"] + player_actions["raises"])/num_hands)
    pfr = round(100 * player_actions["raises"] / num_hands)
    if player in threebets:
        if can_3bet[player] > 0:
            threebet = round(100 * threebets[player]["raises"]/can_3bet[player])
        else:
            threebet = 0
        got_threebet = threebets[player]["calls"] + threebets[player]["folds"]
        if got_threebet > 0:
            fold_threebet = round(100 * threebets[player]["folds"] / got_threebet)
        else:
            fold_threebet = 0
    else:
        threebet = 0
        fold_threebet = 0


    if player in cbets:
        cbet = round(100 * cbets[player]["bets"] / (cbets[player]["bets"] + cbets[player]["checks"]))
        face_cbet = cbets[player]["calls"] + cbets[player]["raises"] + cbets[player]["folds"]
        if face_cbet > 0:
            fold_cbet = round(100 * cbets[player]["folds"] / face_cbet)
        else:
            fold_cbet = 0
    else:
        cbet = 0
        fold_cbet = 0
    stats[player] = {"vpip": vpip, "pfr": pfr, "3bet": threebet, "fold 3bet": fold_threebet, "cbet": cbet, "fold cbet": fold_cbet}

for player, stat in stats.items():
	print(player, stat)
