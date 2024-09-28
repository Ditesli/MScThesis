import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numba as nb
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '0_Params')) # Append the path
import calculate_mortality_noadap   # Import function to calculate mortality without adaptation
import climate_models_info

''' Define important variables'''
scenarios = ['SSP126', 'SSP245', 'SSP370', 'SSP585']
scenarios_SSP = ['SSP1', 'SSP2', 'SSP3', 'SSP5']
years = np.arange(2015,2105,5)
groups = ['oldest', 'older', 'young']
index = pd.MultiIndex.from_product([groups, scenarios], names=['Age group', 'Scenario'])
results_noadapt = pd.DataFrame(index=index, columns=years)

''' This for loop iterates the climate models, scenarios and years to read the temperature and response functions file'''
for climate_model in climate_models:  # for loop for climate models
    for group in groups: # for loop for the three age groups
        mor_np = calculate_mortality.read_mortality_response(base_path, group) # Read mortality response functions
        for scenario, scenario_SSP in zip(scenarios, scenarios_SSP):  # for loop for the four SSP scenarios
            POP = pd.read_csv(base_path + f'GDP-POP/POP files/POP_{scenario_SSP}_{group}.csv')  # Read population files
            POP = POP[~POP['hierid'].str.contains('ATA|CA-', regex=True)]   # Discard the regions of Antarctica and the Caspian Sea    
            for year in years: # for loop for the years
                SSP = pd.read_csv(f'D:/Climate Models - Bias Corrected/{climate_model}/{scenario}/BC_{climate_model}_{scenario}_{year}.csv')  # Read temp files
                mor_temp = calculate_mortality.calculate_mortality_year(SSP, mor_np) # Calculate relative mortality per region (deaths/100,000)
                mor_temp = mor_temp[~mor_temp['hierid'].str.contains('ATA|CA-', regex=True)]
                total_mortality = np.sum(POP[f'{year}'].to_numpy() * mor_temp['total_mortality'].to_numpy() / 1e5) # Calculate mortality relative to SSP scenario
                relative_mortality = total_mortality * 1e5 /np.sum(POP[f'{year}'].to_numpy())
                results_noadapt.at[(group, scenario), year] = relative_mortality
                print(f'{climate_model} - {group} - {scenario} - {year}')
    results_noadapt.to_csv(f'No adaptation files - Climate models\\Total mortality_No adaptation_{climate_model}.csv')  ### Save files


''' This for loops generate the mortality projections for a specific population projection'''

scenario_SSP = 'SSP2'
for climate_model in climate_models:
    for group in groups:
        mor_np = calculate_mortality.read_mortality_response(base_path, group) # Read mortality response functions 
        POP = pd.read_csv(base_path + f'GDP-POP/POP files/POP_{scenario_SSP}_{group}.csv') # Read population files
        POP = POP[~POP['hierid'].str.contains('ATA|CA-', regex=True)]
        for scenario in scenarios:
            for year in years:
                SSP = pd.read_csv(f'D:/Climate Models - Bias Corrected/{climate_model}/{scenario}/BC_{climate_model}_{scenario}_{year}.csv') # Read temperature file
                mor_temp = calculate_mortality.calculate_mortality_year(SSP, mor_np) # Calculate relative mortality per region (deaths/100,000)
                mor_temp = mor_temp[~mor_temp['hierid'].str.contains('ATA|CA-', regex=True)]
                total_mortality = np.sum(POP[f'{year}'].to_numpy() * mor_temp['total mortality'].to_numpy() / 1e5) # Calculate mortality relative to SSP scenario
                relative_mortality = total_mortality * 1e5 /np.sum(POP[f'{year}'].to_numpy())
                results_noadapt.at[(group, scenario), year] = relative_mortality
                print(f'{climate_model} - {group} - {scenario} - {year}')
    results_noadapt.to_csv(f'No adaptation files - Climate models\\Total mortality_No adaptation_SSP2_{climate_model}.csv')