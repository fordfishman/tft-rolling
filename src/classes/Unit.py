class Unit():
    """
    Simple representation a TFT unit

    Attributes:
        name (str): Name of the unit
        cost (int): Cost of the unit (1-5)
    """
    def __init__(self, name:str, cost:int):
        """
        Unit constructor

        Args:
            name (str): Name of the unit
            cost (unit): Cost of the unit (1-5)
        """
        
        assert cost in [1, 2, 3, 4, 5], "Cost must be between 1 and 5"

        self.name = name
        self.cost = cost
        

