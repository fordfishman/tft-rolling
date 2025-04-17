import requests
import json
import enum
import numpy as np
import plotly.express as px

class BagSizes(enum.Enum):
    
    _1COST = 30
    _2COST = 25
    _3COST = 18
    _4COST = 10
    _5COST = 9


def number_shops(unit, nteam, npool, nother, star, level, shop, disable_print=False, round_to_int=True):
    """
    Calculates the expected number
    of shops until you hit an upgrade (2 or
    3 star).
    ----------------------------------------
    unit (Unit): The desired unit
    nteam (int): Number of desired unit on 
        team
    npool (int or float): Number or percentage 
        of units of the same 
        cost of the desired unit left in the 
        pool
    nother (int): Number of desired unit on
        other boards or benches
    star (int): desired star level of unit
    level (int): Current team level
    shop (Shop): Current shop
    
    """

    if nteam >= 9:
        return "Unit is already 3 starred"

    if star == 3:
        nneeded = 9 - nteam

    elif star == 2:
        nneeded = 3 - nteam % 3
    
    elif star == 1:
        nneeded = 1

    number_needed = nneeded # for printing

    cost = unit.cost

    ntot = [ cost.value for cost in BagSizes ]

    # level shouldn't matter for this
    all_odds = shop.odds
    
    odds = all_odds[level-1]

    cost_odd = odds[cost-1]

    if cost_odd == 0:

        return f"Level too low to find {cost} cost unit"

    nleft = ntot[cost-1] - nteam - nother # number

    if nleft <= 0 or nleft < nneeded:
        return "Not enough units left in pool"

    probs = []
    rolls = []

    while nneeded > 0:

        p = nleft/npool * cost_odd

        probs.append(p)

        rolls.append(1/p)

        nleft -= 1 

        npool -= 1

        nneeded -= 1

    if not disable_print:

        print(f"Probability per shop slot for hitting {number_needed} {unit.name}'s per: ")
        print(probs)
        print(f"Expected number of shop slots to hit {number_needed} {unit.name}'s per: ")
        print(rolls)
        print(f"Expected total number of shop slots to hit {number_needed} {unit.name}s: ")
        print(sum(rolls))
        print(f"Expected total number of shops to hit {number_needed} {unit.name}s: ")
        print(sum(rolls)/5)
    # confidence interval/distribution?
    
    if round_to_int:
        return round(sum(rolls)/5)
    else:

        return round(sum(rolls)/5, 2)


def n_other_shop_distribution(unit, nteam, npool, star, level, shop):
    
    cost = unit.cost
    
    ntot = [ cost.value for cost in BagSizes ][cost-1]
        
    n_not_on_team = ntot - nteam
    
    shops = [ 
             number_shops(
                 unit, 
                 nteam, 
                 npool - n, 
                 n, 
                 star, 
                 level, 
                 shop, 
                 disable_print=True, 
                 round_to_int=False) 
             for n in range(1, n_not_on_team)
             ]
    
    n_left = n_not_on_team - np.arange(1, n_not_on_team)
    
    shops_for_plot = [ rolls for rolls in shops]
    n_left = n_left[:len(shops_for_plot)].astype(str)
    
    fig = px.line(x=n_left, y=shops_for_plot)
    fig.update_layout(
        xaxis_title=f"# of {unit.name}'s left in pool",
        yaxis_title="Expected # of shops",
        title="Effect of # left in pool on expected # of shops",
        template="simple_white"
    )
    fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
    
    return fig

def n_pool_shop_distribution(unit, nteam, nother, star, level, shop, units_per_cost):
    
    cost = unit.cost
    
    ntot = [ cost.value for cost in BagSizes ][cost-1]
    
    ncost = ntot*units_per_cost
        
    shops = [ 
             number_shops(
                 unit, 
                 nteam, 
                 n, 
                 nother, 
                 star, 
                 level, 
                 shop, 
                 disable_print=True, 
                 round_to_int=False) 
             for n in range(ntot, ncost)
             ]
    
    shops_for_plot = [ rolls for rolls in shops ]
    n_pool = np.arange(ntot, ncost) - ntot
    shops_for_plot.reverse()
    n_pool = n_pool[::-1]
    
    fig = px.line(x=n_pool, y=shops_for_plot)
    fig.update_layout(
        xaxis_title=f"# of other {cost}-costs left in pool",
        yaxis_title="Expected # of shops",
        title=f"Effect of {cost}-cost pool size on expected # of shops",
        template="simple_white"
    )
    fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
    
    return fig

def load_units(set_='14'): 
    """
    Load CDragon TFT JSON data 

    Returns dictionary of units sorted by unit cost
    """

    # url to CDragon for TFT latest patch, could change in the future
    url = 'https://raw.communitydragon.org/latest/cdragon/tft/en_us.json'

    r = requests.get(url)

    data = json.loads(r.text)

    units = dict()

    for unit in data['sets'][set_]['champions']:
    
        if unit['cost'] <= 5 and len(unit['traits'])>0:

            if unit['cost'] not in units.keys():
                units[unit['cost']] = [unit['name']]
            
            else:
                units[unit['cost']].append(unit['name'])

    return units

def load_shop_odds():

    """
    Grab shop odds from DDragon
    """

    # url to DDragon for TFT latest patch
    url = 'https://raw.githubusercontent.com/InFinity54/LoL_DDragon/refs/heads/master/latest/data/en_US/tft-shop-drop-rates-data.json'

    r = requests.get(url)

    data = json.loads(r.text)

    shop_odds = list()

    # print(data['data']['Shop'][0])

    for level in data['data']['Shop']:

        level_drop_rates = level['dropRatesByTier'][0:5]

        odds_array = np.array([ cost['rate'] for cost in level_drop_rates ])/100
        shop_odds.append(odds_array)


    return shop_odds