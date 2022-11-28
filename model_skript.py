'''
PyPsa Energiesystem-Modell
Design Wasserstoffbasierter Energiesysteme WiSe 2022

@ author: Alexander Kling

Die Bezugsgröße ist 1 MW
'''

# - - - Imports - -  -
import pypsa
import pandas as pd

# - - - Settings - - - -
SNAPSHOTS = 8760 #no of hours of 1 year

# - - - Parameters - - - -
ELECTROLYSIS_EFFICIENCY = 0.7
ELECTROLYSIS_CAPITAL_COST = 1e6 # €/MW
ELECTROLYSIS_MARGINAL_COST = 0 # €/MWh

PV_CAPITAL_COST = 1e3 # €/MW
WIND_CAPITAL_COST = 1e3 # €/MW

# - - - Modell Deklaration - - - -
net = pypsa.Network()
net.set_snapshots(SNAPSHOTS)

# - - - Komponenten hinzufügen - - -

net.add('Bus', 'electrical')
net.add('Bus', 'hydrogen')

net.add('Link', 'electrolysis', bus0 = 'electrical', bus1 = 'hydrogen', efficiency = ELECTROLYSIS_EFFICIENCY,
        p_nom_extendable =True, capital_cost = ELECTROLYSIS_CAPITAL_COST, marginal_cost = ELECTROLYSIS_MARGINAL_COST)

net.add('Generator', 'PV', 'electrical', marginal_cost = 0, capital_cost = PV_CAPITAL_COST, p_nom_extendable = True)
net.add('Generator', 'Wind', 'electrical', marginal_cost = 0, capital_cost = WIND_CAPITAL_COST)


