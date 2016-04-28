"""
Colour maps and range settings for defined phenomena in matplotlib.
"""


phenomena = {'air_temperature': ('coolwarm', [('K', (253, 323)),
                                             ('degC', (-30, 40))]),
            'air_pressure': ('brewer_Blues_09', [('Pa', (9e4, 1.1e5))]),
            'air_pressure_at_sea_level': ('brewer_Blues_09',
                                          [('Pa', (9e4, 1.1e5))]),
            'surface_temperature': ('coolwarm', [('K', (253, 323)),
                                                 ('degC', (-30, 40))]),
            'specific_humidity': ('YlGnBu', [('kg kg-1',
                                                         (0, 0.5))]),
            } 

