'''
PyPsa Energiesystem-Modell
Design Wasserstoffbasierter Energiesysteme WiSe 2022

@ author: Alexander Kling

Die Bezugsgröße ist 1 MW
'''
import numpy as np
# - - - Imports - -  -
import pypsa
import pandas as pd
from matplotlib import pyplot as plt

# - - - Error Fixes - - - -
import subprocess
#ret = subprocess.run(["dir", "/p"], shell=True)

# - - - Plot-Setting - - - -
plt.style.use('bmh')
xticks = np.arange(start=0, stop= 8759, step=8760/12)
xlabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
# - - - Settings - - - -
SNAPSHOTS = 8760 #no of hours of 1 year
USE_BATTERY = True

ELECTROLYSIS_MAX_POWER = 1100
PV_MAX_POWER = 250


# - - - Parameters - - - -
ELECTROLYSIS_EFFICIENCY = 0.7
ELECTROLYSIS_CAPITAL_COST = 1060e3 # €/MW

# PV_CAPITAL_COST = 1e3 # €/MW
PV_CAPITAL_COST = 950e3 # €/MW
WIND_CAPITAL_COST = 1400e3 # €/MW
BATTERY_CAPITAL_COST = 180e3 # €/MWh
HYDROGEN_STORE_CAPITAL_COST = 2700 # €/MWh

# - - - Data Imports - - - -
wind_data = pd.read_csv('data/tampico_wind.csv', skiprows=3)['electricity']
pv_data = pd.read_csv('data/tampico_pv.csv', skiprows=3)['electricity']
#demand_data = pd.read_csv('data/transport_demand_test_MW.csv')['0']
demand_data = pd.read_csv('data/transport_demand_container_MW.csv')

#demand_data = pd.read_csv('data/transport_demand_container_MW_monthly.csv')
#demand_data = pd.read_csv('data/transport_demand_container_MW_monthly_less_overhead.csv')
#demand_data = pd.read_csv('data/transport_demand_container_MW_monthly_less_overhead_start_day15.csv')
demand_data = pd.read_csv('data/transport_demand_container_MW_monthly_day15.csv')

# - - - Modell Deklaration - - - -
net = pypsa.Network()
net.set_snapshots(range(SNAPSHOTS))

# - - - Komponenten hinzufügen - - -

net.add('Bus', 'electrical')
net.add('Bus', 'hydrogen')

net.add('Link', 'Electrolysis', bus0 = 'electrical', bus1 = 'hydrogen', efficiency=ELECTROLYSIS_EFFICIENCY,
        p_nom_extendable=True, p_nom_max = ELECTROLYSIS_MAX_POWER, capital_cost=ELECTROLYSIS_CAPITAL_COST)

net.add('Generator', 'PV', bus='electrical', marginal_cost=0, capital_cost=PV_CAPITAL_COST, p_nom_extendable=True,
        p_nom_max = PV_MAX_POWER, p_max_pu=pv_data)
net.add('Generator', 'Wind', bus='electrical', marginal_cost=0, capital_cost=WIND_CAPITAL_COST, p_nom_extendable=True,
        p_max_pu=wind_data)

net.add('Load', 'Hydrogen Transport', bus='hydrogen', p_set=demand_data['Transport_MW'])
net.add('Load', 'Compression', bus='electrical', p_set=demand_data['Compression'])

net.add('Store', 'Hydrogen Storage', bus='hydrogen', capital_cost=HYDROGEN_STORE_CAPITAL_COST, e_nom_extendable=True, e_cyclic=True)

if USE_BATTERY:
        net.add('Store', 'Battery', bus='electrical', capital_cost=BATTERY_CAPITAL_COST,
                e_nom_extendable=True)

# - - - - - SOLVE MODEL - - - - - -
print('start optimization')
net.lopf(pyomo=False, solver_name='gurobi')
print('Finished simulation!')

fig1 = net.generators_t.p.plot(title='Generator & Electrolysis Power', alpha=0.7)
net.links_t.p0.plot(ax=fig1, alpha=0.7)
plt.ylabel('Power in MW')
plt.xticks(xticks,xlabels)
plt.tight_layout()
plt.xlabel('')
plt.show()

fig4 = net.generators_t.p.plot(title='Generator Power', alpha=0.7)
plt.ylabel('Power in MW')
plt.xticks(xticks,xlabels)
plt.tight_layout()
plt.xlabel('')
plt.show()

fig2 = net.stores_t.e['Hydrogen Storage'].plot()
plt.title('Hydrogen Store Filling Level')
plt.ylabel('Energy in MWh')
plt.xlabel('')
plt.xticks(xticks,xlabels)
plt.tight_layout()
plt.show()
if USE_BATTERY:
        net.stores_t.e['Battery'].plot()
        plt.title('Battery Filling Level')
        plt.ylabel('Energy in MWh')
        plt.xlabel('')
        plt.xticks(xticks, xlabels)
        plt.tight_layout()
        plt.show()
        #net.links_t.plot()


# - - - Cost Calculation - - - - -
capital_costs_generation = net.generators.capital_cost*net.generators.p_nom_opt
capital_costs_storage = net.stores.capital_cost*net.stores.e_nom_opt
capital_costs_links = net.links.capital_cost*net.links.p_nom_opt
capital_costs_total = pd.Series(dtype='float64').append(capital_costs_links).append(capital_costs_generation)\
        .append(capital_costs_storage)



capital_costs_total_million = capital_costs_total*1e-6

installed_power_generation = net.generators.p_nom_opt
installed_power_electrolysis = net.links.p_nom_opt
installed_capacity = net.stores.e_nom_opt

print('Installed Generation Power in MW:\n', installed_power_generation)
print('\nInstalled Electrolysis Power:\n', installed_power_electrolysis)
print('\nInstalled Storage Capacity:\n', installed_capacity)

print('Capital Costs in Million €:\n', capital_costs_total_million,'\nTotal:\n',capital_costs_total_million.sum())



