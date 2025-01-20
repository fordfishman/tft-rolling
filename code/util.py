from Unit import Unit
import numpy as np


def number_shops(unit, nteam, npool, nother, star, level):
    """
    Calculates the expected number
    of shopes until you hit an upgrade (2 or
    3 star).
    ----------------------------------------
    unit (Unit): The desired unit
    nteam (int): Number of desired unit on 
        team
    npool (int): Number of units of the cost
        in of the desired unit in the pool
    nother (int): Number of desired unit on
        other boards or benches
    star (int): desiredstar level of desired 
        unit
    level (int): Current team level
    
    """

    if star == 3:
        nneeded = 9 - nteam

    elif star == 2:
        nneeded = 3 - nteam
        assert nneeded > 0, 'you already have a two star'
    
    elif star == 1:
        nneeded = 1

    cost = unit.cost

    ntot = [29, 22, 18, 12, 10]

    all_odds = [
            np.array([1., 0., 0., 0., 0.]),
            np.array([1., 0., 0., 0., 0.]),
            np.array([0.75, 0.25, 0., 0., 0.]),
            np.array([0.55, 0.30, 0.15, 0., 0.]),
            np.array([0.45, 0.33, 0.20, 0.02, 0.]),
            np.array([0.25, 0.40, 0.30, 0.05, 0.]),
            np.array([0.19, 0.30, 0.35, 0.15, 0.01]),
            np.array([0.16, 0.20, 0.35, 0.25, 0.04]),
            np.array([0.09, 0.15, 0.30, 0.30, 0.16]),
            np.array([0.05, 0.10, 0.20, 0.40, 0.25]),
            np.array([0.01, 0.02, 0.12, 0.50, 0.35])
        ]
    
    odds = all_odds[level-1]

    cost_odd = odds[cost-1]

    nleft = ntot[cost-1] - nteam - nother # number

    probs = []
    rolls = []

    while nneeded > 0:

        p = nleft/npool * cost_odd

        probs.append(p)

        rolls.append(1/p)

        nleft -= 1 

        npool -= 1

        nneeded -= 1

    print(probs)
    print(rolls)
    print(sum(rolls))
    print(sum(rolls)/5)
    # confidence interval/distribution?

    return rolls




