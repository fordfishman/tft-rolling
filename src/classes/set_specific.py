from .Unit import Unit
from .Pool import Pool
from .Shop import Shop
from .util import BagSizes


class Unit_(Unit):
    """
    Extended Unit class for testing purposes.
    """
    def __init__(self, name: str, cost: int, traits: list = None) -> None:
        super().__init__(name, cost, traits)
        
class Pool_(Pool):
    """
    Extended Pool class for testing purposes.
    """
    def __init__(self) -> None:
        super().__init__()
        
    def load_units(self, set_:str='15') -> dict: 
        
        return super().load_units(set_)

    def return_unit(self, unit):
        return super().return_unit(unit)
    
    def size(self, cost=None):
        return super().size(cost)
    
    def get_odds(self, unit):
        return super().get_odds(unit)
        
    def new_game(self):
        
        unit_dict = self.load_units()
        
        for i, cost in enumerate(BagSizes):
            
            self.unit_dict[i+1] = [unit['name'] for unit in unit_dict[i+1]]
            
            self.units[i+1] += [Unit(unit['name'], cost=i+1, traits=unit['traits']) for unit in unit_dict[i+1]] * cost.value

        
        
        return None

class Shop_(Shop):
    """
    Extended Shop class for testing purposes.
    """
    def __init__(self, level: int) -> None:
        super().__init__(level)
        
    def fresh_shop(self, pool:Pool) -> None:
        return super().fresh_shop(pool)
    
    def refresh_shop(self, pool):
        return super().refresh_shop(pool)
    
    def shop_names(self) -> list:
        return super().shop_names()
    
    def level_up(self) -> None:
        return super().level_up()
    
    def get_odds(self, unit:Unit, pool:Pool) -> float:
        return super().get_odds(unit, pool)
        
if __name__ == "__main__":
    pool = Pool_()