"""
Created on 15 sept 2025

DS config file NAture paper 2025
based on last update of ENCORE and EXIOBASE

@author: DNB FS-IFA NC5452 (sebastien gallet)
"""
import os
import pandas as pd
import numpy as np

# path list
path_EXIO='I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\downloaded_data\\EXIOBASE 3\\IOT_2022_ixi\\IOT_2022_ixi\\'
path_ENCORE = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\downloaded_data\\ENCORE\\ENCORE files October 2024_072025\\'
path_DS_store = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\DS_Vuln_update\\'
path_ISO = "I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\downloaded_data\\Misc_tables\\"
Nature_indice_path = "I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2024\\DATA\\DS_code\\ND-GAIN index\\resources\\vulnerability\\"
path_to_file= path_ENCORE + '06. Dependency mat ratings.csv'
isic2nace_raw_path = path_ENCORE + '14. EXIOBASE NACE ISIC crosswalk.csv'
EXIOBASE_A_matrix_path = path_EXIO + "A.csv"
Z_path = path_EXIO + "Z.csv"
X_path = path_EXIO + "x.csv"
adj_ind_file = 'ROE_ROA_debt_ratio per NACE lvl1\\Adj_ind_by_industry.xlsx'
tab_area_country_code = pd.read_csv(path_ISO+'regions_ISO2_continent_area.csv')
os.chdir(path_DS_store)
#######################################
# options rating mapping
rating_mapping_linear = {'ND': 0, 'VL': 0.2, 'L': 0.4, 'M': 0.6, 'H': 0.8, 'VH': 1}
# options
rating_mapping_exp = {'ND': 0, 'VL': 0.06, 'L': 0.13, 'M': 0.25, 'H': 0.5, 'VH': 1}
rating_mapping_S = {'ND': 0, 'VL': 0.06, 'L': 0.2, 'M': 0.8, 'H': 0.94, 'VH': 1}
# retained
rating_mapping = rating_mapping_linear
#########################################
# shocks definition
data_shock = {
    "Area": [
        'European Union (EU)',
        'North America',
        'South America',
        'Sub-Saharan Africa',
        'Middle East & North Africa (MENA)',
        'East Asia',
        'South Asia',
        'Southeast Asia',
        'Oceania',
        'Central Asia',
        'Eastern Europe (non-EU)'],
    "Production shock": [
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1] }
data_shock = pd.DataFrame(data_shock)
# split gov/NFC in Fin portfolio across countries (to be modified)
ratio_Gov_on_NFCpGov=0.2
# activation of alternative definition of gov and finance Vulnerability score
activation_gov_vuln=0;activation_fin_vuln=0

