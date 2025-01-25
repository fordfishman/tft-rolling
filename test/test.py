import unittest
import numpy as np
import sys
import os


current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
sys.path.append(os.path.join(current_directory, '../code'))
from Unit import Unit
from Pool import Pool
from Shop import Shop


class TestUnit(unittest.TestCase):
    """Testing Unit class"""
    def test_attributes(self):

        unit_name = 'Amumu'
        unit_cost = 1

        unit = Unit(unit_name, unit_cost)

        self.assertEqual(unit.name, unit_name, 'Unit name not set correctly')
        self.assertEqual(unit.cost, unit_cost, 'Unit cost not set correctly')

class TestPool(unittest.TestCase):
    """Testing Pool class"""

    def setUp(self):
        self.pool = Pool()

    def test_pool_size(self):

        num_cost = (14, 13, 13, 12, 8, 3)
        bag_sizes = (30, 25, 18, 10, 9, 9)

        for i in range(1, 7): # testing that each pool size is correct
            self.assertEqual(self.pool.size(i), num_cost[i-1]*bag_sizes[i-1], 'Pool size for {} cost not correct'.format(i))

        # testing total pool size is correct
        self.assertEqual(self.pool.size(), np.dot(num_cost, bag_sizes), 'Pool size not correct')
       
    def test_get_unit(self):
    
        for i in range(1, 7): # testing that removing a unit from each cost reduces pool size
            cost_pool_size = self.pool.size(i)
            unit = self.pool.get_unit(i)
            # self.assertEqual(unit.cost, i, 'Unit cost not correct')
            self.assertEqual(self.pool.size(i), cost_pool_size-1, 'Pool size for {} cost not correct after get_unit'.format(i))
            self.pool.return_unit(unit) # return unit to pool

    def test_return_unit(self):

        for i in range(1, 7):

            cost_pool_size = self.pool.size(i)
            unit = self.pool.get_unit(i)
            self.pool.return_unit(unit)
            self.assertEqual(self.pool.size(i), cost_pool_size, 'Pool size for {} cost not correct after return_unit'.format(i))

    def test_odds(self):

        example_units = (Unit('Amumu', 1), Unit('Vander', 2), Unit('Smeech', 3), Unit('Corki', 4), Unit('Sevika', 5), Unit('Viktor', 6))
        num_cost = (14, 13, 13, 12, 8, 3)
        bag_sizes = (30, 25, 18, 10, 9, 9)

        for i in range(1, 7):

            unit_test = example_units[i-1]
            odds_before = self.pool.get_odds(unit_test)

            unit = self.pool.get_unit(i)
            odds_after_get = self.pool.get_odds(unit)


            self.assertEqual(odds_after_get, (bag_sizes[i-1]-1)/(bag_sizes[i-1]*num_cost[i-1]-1), 'Odds for {} cost not correct'.format(i))
            self.assertLess(odds_after_get, odds_before, 'Odds not for {} cost reduced after get_unit'.format(i))
            
            # test odds after return
            self.pool.return_unit(unit)
            odds_after_return = self.pool.get_odds(unit)
            
            self.assertGreater(odds_after_return, odds_after_get, 'Odds not for {} cost increased after return_unit'.format(i))

class TestShop(unittest.TestCase):

    def setUp(self):
        self.shops = [Shop(i) for i in range(1, 12)]
        self.pool = Pool()

    # def test_shop_class(self):
    #     from Shop import Shop

    #     level = 1

    #     shop = Shop(level)

        
if __name__ == '__main__':
    unittest.main()


