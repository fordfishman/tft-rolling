import numpy as np
import requests
import json
from .Unit import Unit
from .util import BagSizes

class Pool():
    """
    Collection of units available to the player.
    
    Attributes:
        units (dict): Dictionary of all units available to the player.
            Keys are cost levels (1-5) and values are lists of Unit objects.
        unit_dict (dict): Dictionary of unique units available in the game.
            Keys are cost levels (1-5) and values are lists of unit names.
    """

    def __init__(self) -> None:
        """
        Loads units and initializes pool according to bag sizes.
        """
        self.units = {i:[] for i in range(1,6)}
        self.unit_dict = dict()
        self.new_game()

    def new_game(self) -> None:
        """
        Initializes the pool with the correct number of units
        for each cost level. The number of units is determined by 
        how many units are in the game and the bag sizes for each 
        cost level.

        Returns:
            None
        """
        
        unit_dict = self.__load_units()
        
        for i, cost in enumerate(BagSizes):
            
            self.unit_dict[i+1] = [unit['name'] for unit in unit_dict[i+1]]
            
            self.units[i+1] += [Unit(unit['name'], cost=i+1, traits=unit['traits']) for unit in unit_dict[i+1]] * cost.value
                
        
        return None
    
    def __load_units(self, set_:str='14') -> dict: 
        """
        Load CDragon TFT JSON data, which contains all units
        and their costs. Traitless and 0 cost units are removed.

        Args:
            set_ (str): Set number to load. Default is current set.
        
        Returns: 
            dict: Dictionary of unit data sorted by unit cost
        """

        # url to CDragon for TFT latest patch, could change in the future
        url = 'https://raw.communitydragon.org/latest/cdragon/tft/en_us.json'

        r = requests.get(url)

        data = json.loads(r.text)

        units = dict()

        for unit in data['sets'][set_]['champions']:
        
            if unit['cost'] <= 5 and len(unit['traits'])>0:

                if unit['cost'] not in units.keys():
                    units[unit['cost']] = [unit]
                
                else:
                    units[unit['cost']].append(unit)

        return units

    def get_unit(self, cost:int) -> Unit:
        """
        Get a random unit of a cost and return it, 
        removing it from the pool.
        
        Args:
            cost (int): Cost of unit to get. Must be 1, 2, 3, 4, or 5.
            
        Returns:
            Unit: Random unit of the specified cost.
        """
        
        assert cost in [1, 2, 3, 4, 5], "Cost must be 1, 2, 3, 4, or 5."

        unit = np.random.choice(self.units[cost])

        self.units[cost].remove(unit)

        return unit

    def return_unit(self, unit:Unit) -> None:
        """
        Return a unit to the pool. This simulates a unit being
        sold.

        Args:
            Unit: The unit to return to the pool. Must be a Unit object.

        Returns:
            None
        """

        self.units[unit.cost].append(unit)

        return None
    
    def size(self, cost=None) -> int:
        """
        Getter for size of pool
        
        Args:
            cost (int): If 1, 2, 3, 4, or 5, is 
                provided, will return the size of the 
                pool for that cost only. When None (default), 
                returns size of whole pool.
        
        Returns:
            int: Size of pool
        
        """
        
        n = 0

        if cost is None: # if no cost provided

            for cost_ in self.units.values():
                n += len(cost_)

        else:
            n = len(self.units[cost])
        
        return n

    
    def get_odds(self, unit:Unit) -> float:

        """ 
        Odds of getting a specific unit from a cost level.
        The odds are equal to the proportion of a cost pool that 
        are that unit.
        
        Args:
            unit (Unit): The unit to get the odds for. Must be a Unit object.
            
        Returns:
            float: Odds of getting the unit from the pool.
        """
        count = sum([ 1 for unit_shop in self.units[unit.cost] if unit.name==unit_shop.name])

        return count/len(self.units[unit.cost])
        







