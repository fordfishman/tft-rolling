from Unit import Unit
from Pool import Pool
import numpy as np

class Shop():

    def __init__(self, level:int) -> None:
        self.__level = level
        self.slots = [ None for i in range(5) ]
        self.odds = [
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
    
    def fresh_shop(self, pool) -> None:

        odds = self.odds[self.__level-1] # level index 1


        for i in range(5):

            cost = np.random.choice(range(1,6), p=odds)

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



