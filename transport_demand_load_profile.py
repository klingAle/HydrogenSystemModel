import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# - - - - Constants - - -

HEIZWERT_H2_MJ = 120  # MJ/kg
HEIZWERT_H2_kWh = 39.39  # kWh/kg


# - - - - Demand Settings - - -
ship_capacity_m3 = 140000  # m^3

liquid_h2_volume_to_kg = 0.7

ship_capacity_kg = ship_capacity_m3*liquid_h2_volume_to_kg

no_of_pumps = 8
pump_capacity = 2000  # m^3/h

loading_flow_m3 = pump_capacity*no_of_pumps
loading_flow_kg = loading_flow_m3*liquid_h2_volume_to_kg
loading_time = round(ship_capacity_m3/loading_flow_m3)

power_flow_h2 = loading_flow_kg*HEIZWERT_H2_kWh


loading_interval_days = 16

start_day = 3
start_hour = start_day*24

load = np.zeros(8760)

for loading_start_time in np.arange(start_hour, 8760, loading_interval_days*24):
    for loading_hour in np.arange(loading_time):
        actual_hour=loading_start_time+loading_hour
        load[actual_hour] = power_flow_h2
        print(load)
plt.plot(load)
load = pd.Series(load)
plt.show()
print(load)
load.to_csv('data/transport_demand_test.csv')

