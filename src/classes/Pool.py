from .Unit import Unit
import numpy as np
from .util import load_units, BagSizes

class Pool():

    def __init__(self) -> None:
        self.units = {i:[] for i in range(1,7)}
        self.unit_dict = load_units()
        self.new_game()



    def new_game(self) -> None:
        
        for i in range(BagSizes._1COST.value):
            self.units[1] += [Unit(unit_name, cost=1) for unit_name in self.unit_dict[1]]
        
        for i in range(BagSizes._2COST.value):
            self.units[2] += [Unit(unit_name, cost=2) for unit_name in self.unit_dict[2]]

        for i in range(BagSizes._3COST.value):
            self.units[3] += [Unit(unit_name, cost=3) for unit_name in self.unit_dict[3]]
            
        for i in range(BagSizes._4COST.value):
            self.units[4] += [Unit(unit_name, cost=4) for unit_name in self.unit_dict[4]]

        for i in range(BagSizes._5COST.value):
            self.units[5] += [Unit(unit_name, cost=5) for unit_name in self.unit_dict[5]]
        
        
        return None

    def get_unit(self, cost) -> Unit:
        """
        Get a random unit of a cost and return it, 
        removing it from the pool
        """

        unit = np.random.choice(self.units[cost])

        self.units[cost].remove(unit)

        return unit

    def return_unit(self, unit:Unit) -> None:

        self.units[unit.cost].append(unit)

        return None
    
    def size(self, cost=None) -> int:
        """
        Returns size of pool
        ---------------------------
        cost (int): If 1, 2, 3, 4, or 5, is 
            provided, will return the size of the 
            pool for that cost only. When None (default), 
            returns size of whole pool.
        """
        
        n = 0

        if cost is None: # if no cost provided

            for cost_ in self.units.values():
                n += len(cost_)

        else:
            n = len(self.units[cost])
        
        return n

    
    def get_odds(self, unit) -> float:

        """ 
        Odds of getting one unit per cost level
        """
        count = sum([ 1 for unit_shop in self.units[unit.cost] if unit.name==unit_shop.name])

        return count/len(self.units[unit.cost])
        







