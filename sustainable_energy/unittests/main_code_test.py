from map_creator.main_code import *
from unittest import TestCase

class test_main(TestCase):

    def test_get_lat_long(self):
        self.assertEqual(len(get_lat_long(49, 24, 100)), 33)
        self.assertEqual(len(get_lat_long(48, 24, 100)), 33)
        self.assertEqual(len(get_lat_long(0, 0, 100)), 0)
    
    def test_get_historical_data(self):
        self.assertTrue(type(get_historical_data(49, 24, "wind")) == LinkedList)
        self.assertTrue(type(get_historical_data(49, 24, "solar")) == LinkedList)
        self.assertEqual(len(get_historical_data(0, 0, "wind")), 3 )
        self.assertEqual(len(get_historical_data(0, 0, "solar")), 3)
        
    def test_get_forecast_data(self):
        self.assertTrue(type(get_forecast_data(49, 24, "wind")) == LinkedList)
        self.assertTrue(type(get_forecast_data(49, 24, "solar")) == LinkedList)
        self.assertEqual(len(get_forecast_data(0, 0, "wind")), 8)
        self.assertEqual(len(get_forecast_data(0, 0, "solar")), 8)
    
    def test_calculate_efficiency(self):
        historical_data = get_historical_data(49, 45, "wind")
        self.assertTrue(type(calculate_efficiency(historical_data, "wind")[0]) == float)
        self.assertTrue(type(calculate_efficiency(historical_data, "wind")[1]) == str)