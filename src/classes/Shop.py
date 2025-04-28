import numpy as np
import requests
import json
from .Unit import Unit
from .Pool import Pool

class Shop():
    """
    Representation of a shop in TFT. 
    
    Attributes:
        slots (list): List of units in the shop.
        odds (list): List of odds for each cost and level.
        __level (int): Current team level.
    """

    def __init__(self, level:int) -> None:
        """
        Initializes the shop with a given level and loads shop odds

        Args:
            level (int): _description_
        """
        self.__level = level
        self.slots = [ None for i in range(5) ]
        self.odds = self.__load_shop_odds()
        
    def __load_shop_odds(self) -> list:

        """
        Uses requests to grab shop odds from DDragon for each level
        
        Returns:
            list: Odds of getting each cost in the shop at each level.
        """

        # url to DDragon for TFT latest patch
        url = 'https://raw.githubusercontent.com/InFinity54/LoL_DDragon/refs/heads/master/latest/data/en_US/tft-shop-drop-rates-data.json'

        r = requests.get(url)

        data = json.loads(r.text)

        shop_odds = list()

        for level in data['data']['Shop']:

            level_drop_rates = level['dropRatesByTier'][0:5]

            odds_array = np.array([ cost['rate'] for cost in level_drop_rates ])/100
            shop_odds.append(odds_array)


        return shop_odds
    
    def fresh_shop(self, pool:Pool) -> None:
        """
        Fills the shop with different units from the pool 
        according to self.odds()

        Args:
            pool (Pool): The unit pool to draw from.

        Returns:
            None
        """

        odds = self.odds[self.__level-1] # level index 1

        for i in range(5):

            cost = np.random.choice(range(1,6), p=odds)

            self.slots[i] = pool.get_unit(cost)
        
        return None
    
    def refresh_shop(self, pool:Pool) -> None:
        """
        Returns current units in shop to the pool and fills 
        the shop with new units.

        Args:
            pool (Pool): The unit pool to draw from.
            
        Returns:
            None
        """

        for unit in self.slots:

            pool.return_unit(unit)
        
        self.slots = [ None for i in range(5) ]

        self.fresh_shop(pool)

        return None


    def shop_names(self) -> list:
        """
        Gets the names of the units in the shop.

        Returns:
            list: Names of units in the shop.
        """

        return [unit.name for unit in self.slots]
    
    def level_up(self) -> None:
        """
        Increase level by 1

        Returns:
            None
        """
        self.__level += 1
        return None
    
    def get_odds(self, unit:Unit, pool:Pool) -> float:
        """
        Odds of getting a specific unit from the shop. The odds account for 
        odds of rolling that cost as well as the proportion of units in the pool
        of the same cost that are that unit.

        Args:
            unit (Unit): The desired unit. 
            pool (Pool): The unit pool to draw from.

        Returns:
            float: The odds of getting the desired unit from the shop.
        """
        
        odds = 0

        if True:

            odds = pool.get_odds(unit) * self.odds[self.__level-1][unit.cost-1]

        return odds



