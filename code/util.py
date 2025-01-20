from Unit import Unit
import numpy as np
import requests
import json


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


def load_units(): 
    """
    Load CDragon TFT JSON data 

    Returns dictionary of units sorted by unit cost
    """

    # url to CDragon for TFT latest patch, could change in the future
    url = 'https://raw.communitydragon.org/latest/cdragon/tft/en_us.json'

    r = requests.get(url)

    data = json.loads(r.text)

    units = dict()

    for unit in data['sets']['13']['champions']:
    
        if unit['cost'] <= 6 and len(unit['traits'])>0:

            if unit['cost'] not in units.keys():
                units[unit['cost']] = [unit['name']]
            
            else:
                units[unit['cost']].append(unit['name'])

    return units

def load_shop_odds():

    """
    Grab shop odds from DDragon
    May need to update with 6 costs or other changes
    """

    # url to DDragon for TFT latest patch
    url = 'https://raw.githubusercontent.com/InFinity54/LoL_DDragon/refs/heads/master/latest/data/en_US/tft-shop-drop-rates-data.json'

    r = requests.get(url)

    data = json.loads(r.text)

    shop_odds = list()

    print(data['data']['Shop'][0])

    for level in data['data']['Shop']:

        level_drop_rates = level['dropRatesByTier']

        odds_array = np.array([ cost['rate'] for cost in level_drop_rates ])
        shop_odds.append(odds_array)


    return shop_odds