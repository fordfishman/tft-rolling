from Unit import Unit
import numpy as np

class Pool():

    def __init__(self) -> None:
        self.units = {i:[] for i in range(1,6)}
        self.new_game()



    def new_game(self) -> None:
        unit_dict = {
            1:["Cassiopeia", "Cho'Gath", "Irelia", "Jhin", "Kayle", "Malzahar", "Maokai", "Orianna", "Poppy", "Renekton", "Samira", "Tristana", "Viego"],
            2:["Ashe", "Galio", "Jinx", "Kassadin", "Kled", "Sett", "Soraka", "Swain", "Taliyah", "Teemo", "Vi", "Warwick", "Zed"],
            3:["Akshan", "Darius", "Ekko", "Garen", "Jayce", "Kalista", "Karma", "Katarina", "Lissandra", "Rek'Sai", "Sona", "Taric", "Vel'Koz"],
            4:["Aphelios", "Azir", "Gwen", "Jarvan IV", "Kai'Sa", "Lux", "Nasus", "Sejuani", "Shen", "Urgot", "Yasuo", "Zeri"],
            5:["Aatrox", "Ahri", "Bel'veth", "Heimerdinger", "K'Sante", "Ryze", "Senna", "Sion"]}
        
        
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
    
    def size(self) -> int:

        n = 0

        for cost in self.units.values():
            n += len(cost)
        
        return n
        







