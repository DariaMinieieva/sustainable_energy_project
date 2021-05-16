from unittest import TestCase
from map_creator.adt_realization import SolarPanels, WindTurbine


class test_adt(TestCase):
    def setUp(self) -> None:
        self.solar = SolarPanels(
            "2021-04-03 16:57:43", "2021-04-03 03:56:12", 36, temperature=7.85)
        self.wind1 = WindTurbine(1, 230)
        self.wind2 = WindTurbine(5, 280)

    def test_solar_calculate_power(self):
        self.assertEqual(self.solar.calculate_power(), 2.439375)
        self.assertEqual(self.solar.calculate_power(500), 4.87875)

    def test_solar_temperature_impact(self):
        self.solar.calculate_power()
        self.assertEqual(self.solar.temperature_impact(), 2.8577278125)
    
    def test_wind_efficiency(self):
        self.assertEqual(self.wind1.wind_efficiency(), -1)
        self.assertEqual(self.wind2.wind_efficiency(), 1)
    
    def test_wind_direction_to_rotate(self):
        self.assertEqual(self.wind1.direction_to_rotate(), 'northeast')
        self.assertEqual(self.wind2.direction_to_rotate(), 'east')
