'''
This class contains realization of an ADT
'''

import time


class SolarPanels:
    def __init__(self, sunset=None, sunrise=None, clouds=None, snow=None, temperature=None, uv=None):
        '''
        Get data
        '''
        self._sunset = sunset
        self._sunrise = sunrise
        self._clouds = clouds
        self._snow = snow
        self._temperature = temperature
        self._uv = uv
        self._power = None

    def set_sunset(self, value):
        '''
        Set sunset hour
        '''
        self._sunset = value

    def set_sunrise(self, value):
        '''
        Set sunrise hour
        '''
        self._sunrise = value

    def set_clouds(self, value):
        '''
        Set clouds value
        '''
        self._clouds = value

    def set_snow(self, value):
        '''
        Set snow value
        '''
        self._snow = value

    def set_temperature(self, value):
        '''
        Set temperature value
        '''
        self._temperature = value

    def set_uv(self, value):
        '''
        Set ultraviolet radiation value
        '''
        self._uv = value

    def get_sunset(self):
        '''
        Get sunset hour
        '''
        return self._sunset

    def get_sunrise(self):
        '''
        Get sunrise hour
        '''
        return self._sunrise

    def get_clouds(self):
        '''
        Get clouds value
        '''
        return self._clouds

    def get_snow(self):
        '''
        Get snow value
        '''
        return self._snow

    def get_temperature(self):
        '''
        Get temperature value
        '''
        return self._temperature

    def get_uv(self):
        '''
        Get ultraviolet radiation value
        '''
        return self._uv

    def get_power(self):
        '''
        Get power value
        '''
        return self._power

    def calculate_power(self, watts=250):
        '''
        Calculate power of a solar panel in kilowatts
        '''
        sunrise_hour = self.get_sunrise()[11:]
        sunset_hour = self.get_sunset()[11:]

        average_hour = int(sunset_hour[:2]) - int(sunrise_hour[:2])

        average_hour += (int(sunset_hour[3:5]) - int(sunrise_hour[3:5])) / 100

        self._power = (watts * average_hour * 0.75) / 1000

        return self._power

    def temperature_impact(self):
        '''
        If temperature is higher than 25 degrees celcius(77 Fahrenheit)
        its efficiency decreases by 1 % every degree and increase
        if temperature is below that point
        '''
        indx = self._temperature - 25

        if indx > 0:
            self._power *= 1 - indx / 100
        else:
            self._power *= 1 + abs(indx) / 100

        return self._power

    def __str__(self):
        return f"{self._sunset}, {self._sunrise}, {self._temperature}, {self._power}"


class WindTurbine:
    def __init__(self, wnd_speed=None, wnd_degree=None):
        '''
        Set data
        '''
        self._wnd_speed = wnd_speed
        self._wnd_degree = wnd_degree

        self._wind_efficiency_level = None
        self._turbine_direction = None

    def set_wnd_speed(self, value):
        '''
        Set wind speed
        '''
        self._wnd_speed = value

    def set_wnd_degree(self, value):
        '''
        Set wind direction
        '''
        self._wnd_degree = value

    def get_wnd_speed(self):
        '''
        Get wind speed
        '''
        return self._wnd_speed

    def get_wnd_degree(self):
        '''
        Get wind direction
        '''
        return self._wnd_degree

    def wind_efficiency(self):
        '''
        -1 - not enough speed
        0 - minimum required speed
        1 - optimal speed
        2 - high performance speed
        3 - maximum speed, wind turbine is uneffective
        '''

        if self._wnd_speed < 2:
            self._wind_efficiency_level = -1

        elif 2 <= self._wnd_speed < 3.5:
            self._wind_efficiency_level = 0

        elif 3.5 <= self._wnd_speed < 10:
            self._wind_efficiency_level = 1

        elif 10 <= self._wnd_speed < 15:
            self._wind_efficiency_level = 2

        elif 15 <= self._wnd_speed <= 25:
            self._wind_efficiency_level = -1

        return self._wind_efficiency_level

    def direction_to_rotate(self):
        '''
        Determine the direction to put a face of turbine
        '''
        if self._wnd_degree < 22.5 or self._wnd_degree >= 337.5:
            self._turbine_direction = "south"
        elif 22.5 <= self._wnd_degree < 67.5:
            self._turbine_direction = "southwest"
        elif 67.5 <= self._wnd_degree < 112.5:
            self._turbine_direction = "west"
        elif 122.5 <= self._wnd_degree < 157.5:
            self._turbine_direction = "northwest"
        elif 157.5 <= self._wnd_degree < 202.5:
            self._turbine_direction = "north"
        elif 202.5 <= self._wnd_degree < 247.5:
            self._turbine_direction = "northeast"
        elif 247.5 <= self._wnd_degree < 292.5:
            self._turbine_direction = "east"
        elif 292.5 <= self._wnd_degree < 337.5:
            self._turbine_direction = "southeast"

        return self._turbine_direction

    def __str__(self):
        return f"{self._wnd_degree}, {self._wnd_speed}, {self._wind_efficiency_level}, {self._turbine_direction}"


if __name__ == "__main__":
    a = SolarPanels(sunset="2021-04-09 17:00:02",
                    sunrise="2021-04-09 12:00:25", temperature=7.91)
    print(a.calculate_power())
    print(a.temperature_impact())

    b = WindTurbine(4.72, 226)
    print(b.wind_efficiency())
    print(b.direction_to_rotate())
