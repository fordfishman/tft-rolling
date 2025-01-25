import numpy as np
import requests
import json


def number_shops(unit, nteam, npool, nother, star, level, shop):
    """
    Calculates the expected number
    of shops until you hit an upgrade (2 or
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
    shop (Shop): Current shop
    
    """

    if star == 3:
        nneeded = 9 - nteam

    elif star == 2:
        nneeded = 3 - nteam
        assert nneeded > 0, 'you already have a two star'
    
    elif star == 1:
        nneeded = 1

    cost = unit.cost

    ntot = [30, 25, 18, 10, 9, 9]

    # level shouldn't matter for this
    all_odds = shop.odds
    
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

        odds_array = np.array([ cost['rate'] for cost in level_drop_rates ])/100
        shop_odds.append(odds_array)


    return shop_odds