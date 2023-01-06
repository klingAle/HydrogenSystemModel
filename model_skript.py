'''
PyPsa Energiesystem-Modell
Design Wasserstoffbasierter Energiesysteme WiSe 2022

@ author: Alexander Kling

Die Bezugsgröße ist 1 MW
'''

# - - - Imports - -  -
import pypsa
import pandas as pd
from matplotlib import pyplot as plt

# - - - Error Fixes - - - -
import subprocess
#ret = subprocess.run(["dir", "/p"], shell=True)

# - - - Settings - - - -
SNAPSHOTS = 8760 #no of hours of 1 year
USE_BATTERY = True

# - - - Parameters - - - -
ELECTROLYSIS_EFFICIENCY = 0.7
ELECTROLYSIS_CAPITAL_COST = 500e3 # €/MW
ELECTROLYSIS_MARGINAL_COST = 0 # €/MWh

# PV_CAPITAL_COST = 1e3 # €/MW
PV_CAPITAL_COST = 648e3 # $/MW
WIND_CAPITAL_COST = 1.3e6 # €/MW
BATTERY_CAPITAL_COST = 135e3 # $/MWh
HYDROGEN_STORE_CAPITAL_COST = 2700 # €/MWh

# - - - Data Imports - - - -
wind_data = pd.read_csv('data/tampico_wind.csv', skiprows=3)['electricity']
pv_data = pd.read_csv('data/tampico_pv.csv', skiprows=3)['electricity']
demand_data = pd.read_csv('data/transport_demand_test.csv')['0']

# - - - Modell Deklaration - - - -
net = pypsa.Network()
net.set_snapshots(range(SNAPSHOTS))

# - - - Komponenten hinzufügen - - -

net.add('Bus', 'electrical')
net.add('Bus', 'hydrogen')

net.add('Link', 'electrolysis', bus0 = 'electrical', bus1 = 'hydrogen', efficiency=ELECTROLYSIS_EFFICIENCY,
        p_nom_extendable=True, p_nom_max = 100e3, capital_cost=ELECTROLYSIS_CAPITAL_COST, marginal_cost=ELECTROLYSIS_MARGINAL_COST)

net.add('Generator', 'PV', bus='electrical', marginal_cost=0, capital_cost=PV_CAPITAL_COST, p_nom_extendable=True,
        p_nom_max = 100e3, p_max_pu=pv_data)
net.add('Generator', 'Wind', bus='electrical', marginal_cost=0, capital_cost=WIND_CAPITAL_COST, p_nom_extendable=True,
        p_max_pu=wind_data)

net.add('Load', 'Hydrogen Transport', bus='hydrogen', p_set=demand_data)

net.add('Store', 'Hydrogen Storage', bus='hydrogen', capital_cost=HYDROGEN_STORE_CAPITAL_COST, e_nom_extendable=True)

if USE_BATTERY:
        net.add('Store', 'Battery', bus='electrical', capital_cost=BATTERY_CAPITAL_COST,
                e_nom_extendable=True)

# - - - - - SOLVE MODEL - - - - - -
print('start optimization')
net.lopf(pyomo=False, solver_name='gurobi')
print('Finished simulation!')
net.generators_t.p.plot()
net.stores_t.e.plot()

print(net.stores,net.links, net.generators)


'''fig, axes = plt.subplots(2)
net.links_t.'''


plt.show()


