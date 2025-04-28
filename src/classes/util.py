import enum
import numpy as np
import plotly.express as px
from scipy.signal import convolve
from scipy.stats import geom



class BagSizes(enum.Enum):
    """
    Bag sizes for each cost level in TFT represented as an enum.
    """
    
    _1COST = 30
    _2COST = 25
    _3COST = 18
    _4COST = 10
    _5COST = 9

def process_state(unit, nteam:int, nother:int, star:int, level:int, shop) -> tuple:
    """
    Intermediate function to process how many of a certain unit are
    one a team, how many are out of the pool, how many are desired, and 
    what the odds of rolling the unit are.

    Args:
        unit (Unit): Unit being rolled for
        nteam (int): Number of desired unit already purchased
        nother (int): Number of desired unit on other boards or benches
        star (int): Desired star level of desired unit
        level (int): Current team level
        shop (Shop): A shop object used to get odds for a certiain level

    Returns:
        nneeded (int): Number of copies of the unit needed to reach the desired star level
        nleft (int): Number of unit copies left in the pool
        cost (int): cost of the unit
        cost_odd (float): Odds of a shop slot rolling the cost as the desired unit
    """
    
    if nteam >= 9:
        nneeded = 0

    if star == 3:
        nneeded = 9 - nteam

    elif star == 2:
        nneeded = 3 - nteam % 3
    
    elif star == 1:
        nneeded = 1
        
    cost = unit.cost
    ntot = [ cost.value for cost in BagSizes ]
    all_odds = shop.odds 
    odds = all_odds[level-1]
    cost_odd = odds[cost-1]
    nleft = ntot[cost-1] - nteam - nother # number left in pool
    
    return nneeded, nleft, cost, cost_odd

def number_shops(unit, nteam:int, npool:int, nother:int, star:int, level:int, shop, round_to_int=True):
    """
    Calculates the expected number of shops until you reach the desired star level
    for a given unit. The expected number of shops to hit the next copy of the unit 
    is calculated by taking the expectation of a geometric distribution (1/p) where 
    p is the probability of rolling the unit in a shop slot. When multiple copies are 
    needed, this expectation is calculated for as many copies as needed.
    
    Args:
        unit (Unit): Unit being rolled for
        nteam (int): Number of desired unit already purchased
        npool (int): Number or percentage of units of the same cost of the desired 
            unit left in the pool
        nother (int): Number of desired unit on other boards or benches
        star (int): Desired star level of desired unit
        level (int): Current team level
        shop (Shop): A shop object used to get odds for a certiain level
        round_to_int (bool): If True, rounds the expected number of shops to the nearest integer. 
            If False, returns the expected number of shops as a float to the hundredths.
            Default is True.
    
    Returns:
        int or float: Expected number of shops until the desired star level is reached
    """
    
    nneeded, nleft, cost, cost_odd = process_state(unit, nteam, nother, star, level, shop)

    if nneeded == 0:
        return "Unit is already 3 starred"

    number_needed = nneeded # for printing

    if cost_odd == 0:

        return f"Level too low to find {cost} cost unit"

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
    
    if round_to_int:
        return round(sum(rolls)/5)
    else:

        return round(sum(rolls)/5, 2)

def cdf_plot(unit, nteam:int, npool:int, nother:int, star:int, level:int, shop):
    """
    Creates a cumulative distribution function (CDF) plot for the probability of hitting the 
    desired number of copies of a unit in a given number of shop rolls. The probability of 
    hitting the next copy of a unit in a certain amount of shop slots is modeled as geometric process. 
    The CDF is calculated using the convolving the probability mass functions (PMFs) of the 
    geometric distribution for each copy needed. The CDF is then calculated by taking the cumulative 
    sum of the PMF for every 5 shop slots, since a single shop reroll refreshes 5 slots. The CDF is plotted
    using Plotly Express.
    
    Statistics source:  https://www.statlect.com/fundamentals-of-probability/sums-of-independent-random-variables

    Args:
        unit (Unit): Unit being rolled for
        nteam (int): Number of desired unit already purchased
        npool (int): Number or percentage of units of the same cost of the desired 
            unit left in the pool
        nother (int): Number of desired unit on other boards or benches
        star (int): Desired star level of desired unit
        level (int): Current team level
        shop (Shop): A shop object used to get odds for a certain level

    Returns:
        plotly.graph_objects._figure.Figure: Bar plot of the probability of hitting the 
            desired number of copies of a unit in a given number of shop rolls.
    """
    
   
    return_blank = False

    nneeded, nleft, _, cost_odd = process_state(unit, nteam, nother, star, level, shop)  
    
    if nneeded ==0 or cost_odd == 0 or nleft <= 0 or nleft < nneeded:
        return_blank = True
    
    if return_blank:
        
        return px.bar(
            x=[0],
            y=[0],
        )
    
    max_rolls = 1000
    
    rolls = np.arange(1, max_rolls)
    
    p = nleft / npool * cost_odd
    pmf = geom.pmf(rolls, p)
    
    nleft -= 1
    nneeded -= 1
    npool -= 1
    
    while nneeded > 0:
        
        p = nleft / npool * cost_odd
        pmf_i = geom.pmf(rolls, p)
        pmf = convolve(pmf, pmf_i, method='direct')
        
        nleft -= 1
        nneeded -= 1
        npool -= 1
    
    # cumulative sum of pmf for every 5 shop slots, aka a reroll
    cdf = [ sum(pmf[0:i+1])*100 for i in range(5,len(pmf),5) ]
        
    fig = px.bar(x=np.arange(1, len(cdf)+1), y=cdf)
    fig.update_layout(
        title=f"Probability of hitting {star}-star {unit.name} as you roll",
        template="simple_white",
        hovermode="x",
        hoverlabel_font_size=16,
        font_size=14,
        title_font_size=20,
        dragmode=False
    )
    fig.update_xaxes(
        title_text="Shop rolls",
        range=[0, 100],
        tick0=0,
        dtick=20,
        showspikes=True, 
        spikesnap="cursor", 
        spikemode="across",
        spikethickness=0.5,
        )
    fig.update_yaxes(
        title_text="Probability of hitting",
        ticksuffix= "%",
    )
    fig.update_traces(
        hovertemplate="# of shop rolls: %{x}<br>Probability of hitting: %{y:.2f}%",
        marker_color='white', marker_line_color='blue')
    
    return fig


def n_other_shop_distribution(unit, nteam:int, npool:int, star:int, level:int, shop):
    """
    Creates a plot showing the expected number of shops rolls for hitting the desired star level of a unit
    as the number of the desired units are taken out of the pool by other players changes. 

    Args:
        unit (Unit): Unit being rolled for
        nteam (int): Number of desired unit already purchased
        npool (int): Number or percentage of units of the same cost of the desired 
            unit left in the pool
        star (int): Desired star level of desired unit
        level (int): Current team level
        shop (Shop): A shop object used to get odds for a certiain level

    Returns:
        plotly.graph_objects._figure.Figure: Bar plot of expected number of shops rolls
    """
    
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
                 round_to_int=False) 
             for n in range(1, n_not_on_team)
             ]
    
    n_left = n_not_on_team - np.arange(1, n_not_on_team)
    
    shops_for_plot = [ rolls for rolls in shops]
    n_left = n_left[:len(shops_for_plot)].astype(str)
    
    fig = px.bar(x=n_left, y=shops_for_plot)
    fig.update_layout(
        xaxis_title=f"# of {unit.name}'s left in pool",
        yaxis_title="Expected # of shops",
        title="Effect of # left in pool on expected # of shops",
        template="simple_white",
        dragmode=False,
        hovermode="x",
        hoverlabel_font_size=16,
        font_size=14,
        title_font_size=20,
    )
    fig.update_xaxes(
        showspikes=True, 
        spikesnap="cursor", 
        spikemode="across",
        spikethickness=0.5,
    )
    fig.update_traces(
        hovertemplate="# left: %{x}<br>Expected # of shops: %{y}",
        marker_color='white', marker_line_color='blue', marker_line_width=1.5)
    
    return fig

def n_pool_shop_distribution(unit, nteam:int, nother:int, star:int, level:int, shop, units_per_cost:int):
    """
    Creates a plot showing the expected number of shops rolls for hitting the desired star level of a unit
    as the number of units of the same cost in the pool changes.

    Args:
        unit (Unit): Unit being rolled for
        nteam (int): Number of desired unit already purchased
        nother (int): Number of desired unit on other boards or benches
        star (int): Desired star level of desired unit
        level (int): Current team level
        shop (Shop): A shop object used to get odds for a certiain level
        units_per_cost (int): How many units of the same cost are in the pool.

    Returns:
        plotly.graph_objects._figure.Figure: Bar plot showing the expected number of shops rolls
    """
    
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
                 round_to_int=False) 
             for n in range(ntot, ncost)
             ]
    
    shops_for_plot = [ rolls for rolls in shops ]
    n_pool = np.arange(ntot, ncost) - ntot
    shops_for_plot.reverse()
    n_pool = n_pool[::-1]
    
    fig = px.bar(x=n_pool, y=shops_for_plot)
    fig.update_layout(
        xaxis_title=f"# of other {cost}-costs left in pool",
        yaxis_title="Expected # of shops",
        title=f"Effect of {cost}-cost pool size on expected # of shops",
        template="simple_white",
        dragmode=False,
        hovermode="x",
        hoverlabel_font_size=16,
        font_size=14,
        title_font_size=20,
    )
    fig.update_xaxes(
        showspikes=True, 
        spikesnap="cursor", 
        spikemode="across",
        spikethickness=0.5,
    )
    fig.update_traces(
        hovertemplate="# left: %{x}<br>Expected # of shops: %{y}",
        marker_color='white', marker_line_color='blue'
    )
    
    return fig
