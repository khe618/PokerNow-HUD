# PokerNow-HUD

To use, clone this repository, and replace the files in the logs directory with your own full logs downloaded from PokerNow. Then run poker_now.py to output HUD stats for 
each distinct display name in the logs (not case-sensitive). The current metrics tracked are:
VPIP- How often the player voluntarily puts in money preflop, not including the blinds
PFR- How often the player enters preflop with a raise. This number must be no greater than VPIP
3bet- How often the player 3bets, given that they have an opportunity to 3 bet by having a player in front of them raise first in. Squeezes are also
counted towards this metric.
Fold to 3bet- How often the player folds as the initial raiser when getting 3 bet. Note that this also includes when getting squeezed and does not take into consideration
the possibility of a cold 4 bet
Cbet: How often the player bets the flop, given they were the preflop aggressor. Applies to multiway pots, which may skew results. If a player donks into the aggressor, the cbet stat will not be affected for that hand
Fold to Cbet: How often the player folds to a cbet. Applies to multiway pots, which may skew results. If a player raises the cbet, the fold to cbet stat is not affected for that hand
