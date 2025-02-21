from .Unit import Unit
from .Pool import Pool
import numpy as np
from .util import load_shop_odds

class Shop():

    def __init__(self, level:int) -> None:
        self.__level = level
        self.slots = [ None for i in range(5) ]
        self.odds = load_shop_odds()
    
    def fresh_shop(self, pool) -> None:

        odds = self.odds[self.__level-1] # level index 1


        for i in range(5):

            cost = np.random.choice(range(1,7), p=odds)

            self.slots[i] = pool.get_unit(cost)
        
        return None
    
    def refresh_shop(self, pool) -> None:

        for unit in self.slots:

            pool.return_unit(unit)
        
        self.slots = [ None for i in range(5) ]

        self.fresh_shop(pool)



    def shop_names(self) -> list:

        return [unit.name for unit in self.slots]
    
    def level_up(self) -> None:
        self.__level += 1
        return None
    
    def get_odds(self, unit, pool) -> float:
        
        odds = 0

        if True:

            odds = pool.get_odds(unit) * self.odds[self.__level-1][unit.cost-1]

        return odds



