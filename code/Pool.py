from Unit import Unit
import numpy as np

class Pool():

    def __init__(self) -> None:
        self.units = {i:[] for i in range(1,6)}
        self.new_game()



    def new_game(self) -> None:
        unit_dict = {
            1:["Cassiopeia", "Cho'Gath", "Graves", "Illaoi", "Irelia", "Jhin", "Kayle", "Malzahar", "Milio",  "Orianna", "Poppy", "Renekton"],
            2:["Ashe", "Galio", "Jinx", "Kassadin", "Naafiri", "Qiyana", "Sett", "Soraka", "Swain", "Taliyah", "Twisted Fate", "Vi", "Warwick"],
            3:["Darius", "Ekko",  "Jayce",  "Karma", "Katarina", "Miss Fortune", "Nautilus", "Neeko", "Quinn", "Rek'Sai", "Sona", "Taric", "Vel'Koz"],
            4:["Aphelios", "Azir", "Fiora", "Jarvan IV", "Kai'Sa", "Mordekaiser", "Nasus", "Nilah", "Sejuani", "Shen", "Silco", "Xayah"],
            5:["Aatrox", "Ahri", "Bel'veth", "Gangplank", "Heimerdinger", "K'Sante", "Ryze", "Sion"]}
        
        
        for i in range(29):
            self.units[1] += [Unit(unit_name, cost=1) for unit_name in unit_dict[1]]
        
        for i in range(22):
            self.units[2] += [Unit(unit_name, cost=2) for unit_name in unit_dict[2]]

        for i in range(18):
            self.units[3] += [Unit(unit_name, cost=3) for unit_name in unit_dict[3]]
            
        for i in range(12):
            self.units[4] += [Unit(unit_name, cost=4) for unit_name in unit_dict[4]]

        for i in range(10):
            self.units[5] += [Unit(unit_name, cost=5) for unit_name in unit_dict[5]]
        
        return None

    def get_unit(self, cost) -> Unit:

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
        cost (int): If 1, 2, 3, 4, or
            5 is provided, will return the 
            size of the pool for that cost only.
            When None (default), returns size of
            whole pool.
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
        







