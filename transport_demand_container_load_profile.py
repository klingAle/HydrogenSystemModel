import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# - - - - Constants - - -

HEIZWERT_H2_MJ = 120  # MJ/kg
HEIZWERT_H2_kWh = 39.39  # kWh/kg


# - - - - Demand Settings - - -
container_capacity = 1100  # kg

no_of_containers_per_transport = 1800 #350

#no_of_pumps = 8
#pump_capacity = 2000  # m^3/h

total_hydrogen_per_transport = container_capacity*no_of_containers_per_transport
loading_time = 12 # hours

hydrogen_loading_mass_flow = total_hydrogen_per_transport/loading_time # kg/hour

power_flow_h2_MW = hydrogen_loading_mass_flow*HEIZWERT_H2_kWh/1000


loading_interval_days = 30 #7

start_day = 3
start_hour = start_day*24

load = np.zeros(8760)

for loading_start_time in np.arange(start_hour, 8760, loading_interval_days*24):
    for loading_hour in np.arange(loading_time):
        actual_hour=loading_start_time+loading_hour
        load[actual_hour] = power_flow_h2_MW
        print(load)
plt.plot(load)
load = pd.Series(load)

total_energy = sum(load)
print('Total Energy: {}'.format(total_energy))
plt.show()
print(load)
load.to_csv('data/transport_demand_container_MW_monthly.csv')