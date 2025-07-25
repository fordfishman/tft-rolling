from .Unit import Unit
from .Pool import Pool
from .Shop import Shop

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

class Shop_(Shop):
    """
    Extended Shop class for testing purposes.
    """
    def __init__(self, level: int) -> None:
        super().__init__(level)