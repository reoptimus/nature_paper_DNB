# SHSProcess
# code in python from from the NoteBook .ipynb 'shs_nature_analysis_Seb.ipynb'
# flatten code for optimisation and debug
# 11/14/2025 , s.y.a.gallet

import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
import os
from itertools import product
os.getcwd()

instrmnt_df = pd.read_csv('G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv', dtype={'nace':'str'})
instrmnt_df.head(3)

# Read and prep dependency score/vulnerability score
path = 'i:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\DS_Vuln_update\\Vuln_final_store/'
Vuln_final_name = 'Vuln_final_03_11_2025.csv'
Alpha_final_name = 'Alpha_final_03_11_2025.xlsx'

ds_df = pd.read_csv(path+Vuln_final_name)
# I:/FS/FS/Statsp/000-Beleidsmedewerkers/Sebastien Gallet/Biodiv/OS-2025/DS_Vuln_update/Vuln_final_store
# Pivot wide to long
ds_df = ds_df.melt(
    id_vars=['region', 'eco_serv', 'EXIOBASE','indout','NACE Code','Adj_ind'],
    value_vars=ds_df.columns[3:],
    var_name='Vuln_type',
    value_name='Vuln'
)

def extract_prefix(strings):
    return [s.split('_DS_total_')[0].split('_Vuln_total_')[0] for s in strings]

Dependency_type_list = {'DS_total','Vuln_total'}
Scenario_list = extract_prefix(ds_df['Vuln_type'].unique())
Scenario_list = list(set(Scenario_list))
Aggreg_type_list = {'SR','max'}
Eco_serv_list = ds_df['eco_serv'].unique()
ds_df

# Read and prep Alpha and production X from MRIO
# Load data
alpha_df = pd.read_excel(path+Alpha_final_name)
area_map = pd.read_csv('./data/regions_ISO2_continent_area.csv')

# Reshape and merge
alpha_df = (
    alpha_df.melt(id_vars=['Area', 'eco_serv'], var_name='Vuln_type', value_name='Alpha')
            .merge(area_map, left_on='Area', right_on='area', how='left')
            .drop(columns=['Area', 'area'])
)
alpha_df.rename(columns={'eco_serv':'scenario', 'Vuln_type option':'vulnerability_option', 'region':'ISSUER_COUNTRY', 'Alpha':'alpha'}, inplace=True)

# read x.csv to get production per country/sector to weight Vulnerability when multiple EXIOBASE per Nace code
X_df = pd.read_csv("I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\downloaded_data\\EXIOBASE 3\\IOT_2022_ixi\\IOT_2022_ixi\\x.csv")

# merge to get ED2PaR indicator on production loss absolute and relative
df = ds_df[['region', 'EXIOBASE', 'eco_serv', 'Vuln_type', 'indout', 'NACE Code', 'Adj_ind','Vuln']]
# Remove suffix starting with '_xx' followed by any characters and Create a new column with the suffix removed
df['option'] = df['Vuln_type'].str.rsplit('_', n=1).str[1]
df['Vuln_type'] = df['Vuln_type'].str.rsplit('_', n=1).str[0]
alpha_df_clean = alpha_df
alpha_df_clean['Vuln_type'] = alpha_df['Vuln_type'].str.rsplit('_', n=1).str[0]
alpha_df_clean['option'] = alpha_df_clean['Vuln_type'].str.rsplit('_', n=1).str[1]
alpha_df_clean['Vuln_type'] = alpha_df_clean['Vuln_type'].str.rsplit('_', n=1).str[0]

# do merge
df = df.merge(alpha_df_clean.rename(columns={'scenario':'eco_serv','ISSUER_COUNTRY':'region'}), on =['Vuln_type','eco_serv','region','option'], how='left')
df['delta_prod'] = df['indout']*df['Vuln']*df['alpha']
df.head()

import pandas as pd
import matplotlib.pyplot as plt

# Load the mapping file
path = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025'
nace_map = pd.read_excel(path + '/git_repo/Ecosystem_ds/data/nace_0d_map.xlsx', engine='openpyxl')

# Merge with df on 'NACE Code' matching 'nace_2d_code'
df_merge = df.merge(nace_map, left_on='NACE Code', right_on='nace_2d_code', how='left')

# Set your filter values
eco_serv_filter = 'Water flow regulation' # 'Water supply', 'Rainfall pattern regulation' , 'Water purification', 'Pollination' ,'Water flow regulation'
vuln_type_filter = '1_World_shock_10perc_02_GOVonNFC_Vuln_total' # '1_World_shock_10perc_02_GOVonNFC_Vuln_total' . '0_World_shock_10perc_02_GOVonNFC_DS_total', '0_World_shock_10perc_02_GOVonNFC_Vuln_total', '1_EUshock_3perc_08_GOVonNFC_DS_total', '1_EUshock_3perc_08_GOVonNFC_Vuln_total' , '1_World_shock_10perc_02_GOVonNFC_DS_total' , '1_World_shock_3perc_02_GOVonNFC_DS_total'
option_filter = 'SR' # 'SR', 'max'
list_country = ['NL', 'AT', 'BE', 'DE', 'ES', 'FI', 'FR', 'GR', 'HR', 'IT','PL','PT', 'US', 'JP', 'CN', 'CA'] # , 'GB', 'US', 'JP', 'CN', 'CA'

# Filter the data
filtered_df = df_merge[(df_merge['eco_serv'] == eco_serv_filter) &
    (df_merge['Vuln_type'] == vuln_type_filter) &
    (df_merge['option'] == option_filter) &
    (df_merge['region'].isin(list_country) )]

# Aggregate delta_prod and indout
agg_df = filtered_df.groupby(['region', 'nace_0d_code'])[['delta_prod', 'indout']].sum().reset_index()

# Compute relative delta_prod
agg_df['relative_delta_prod'] = agg_df['delta_prod'] / agg_df['indout'] * 100

# Pivot for heatmap
heatmap_data = agg_df.pivot(index='nace_0d_code', columns='region', values='relative_delta_prod').fillna(0) # values='relative_delta_prod'  values='delta_prod'

# Plot heatmap without annotations, inverted color scale (red=min, blue=max)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='BrBG' , cbar_kws={'label': 'Relative delta_prod (%)'}, annot=False) # 'viridis' , 'BrBG' , 'cividis' , 'Blues' # cbar_kws={'label': 'Relative delta_prod (%)'
plt.title(f"Relative delta_prod by NACE Code and Region\n({eco_serv_filter}, {vuln_type_filter}, {option_filter})")
plt.xlabel("Region")
plt.ylabel("NACE Code")
plt.tight_layout()
plt.show()

heatmap_data.to_csv(path+'/analysis/output_data/heatmap_data_nPaR_relat.csv')

from matplotlib.ticker import FuncFormatter
# Pivot for heatmap
heatmap_data = agg_df.pivot(index='nace_0d_code', columns='region', values='delta_prod').fillna(0) # values='relative_delta_prod'  values='delta_prod'
heatmap_data = heatmap_data[heatmap_data.index != 'U']
# Apply log scale to delta_prod values (add small constant to avoid log(0))
heatmap_log = np.log10(-heatmap_data)

# Plot heatmap with colorbar in Meur units
plt.figure(figsize=(10, 6))
ax = sns.heatmap(heatmap_log, cmap='BrBG_r', cbar_kws={'label': 'delta_prod (Meur)'}, annot=False)

# Define a formatter to convert log scale back to Meur units
def log_to_meur(x, pos):
    return f"{10**x:.0f}"

# Apply formatter to colorbar
colorbar = ax.collections[0].colorbar
colorbar.ax.yaxis.set_major_formatter(FuncFormatter(log_to_meur))
plt.title(f"Production loss in Meur \n({eco_serv_filter}, {vuln_type_filter}, {option_filter})")
plt.xlabel("Region")
plt.ylabel("NACE Code")
plt.tight_layout()
plt.show()

heatmap_data.to_csv(path+'/analysis/output_data/heatmap_data_nPaR_abs.csv')

# Merge with alpha and vulnerability score per NACE (EXIOBASE proxy)
def is_missing(val):
    return val is None or (pd.isna(val) if not isinstance(val, (list, pd.Series, pd.DataFrame)) else False)

def compute_weighted_vuln(exiobase_values, vuln_rows_clean):
    # Filter relevant rows in one go
    vuln_filtered = vuln_rows_clean[vuln_rows_clean['EXIOBASE'].isin(exiobase_values)].copy()
    # Merge on EXIOBASE / sector
    merged = vuln_filtered
    # Drop rows with missing values
    merged = merged[['Vuln', 'indout']].drop_duplicates().dropna().copy()
    if not merged.empty:
        if not (merged['indout'] == 0).all():
            weighted_sum = (merged['Vuln'] * merged['indout']).sum()
            total_weight = merged['indout'].sum()
            return weighted_sum / total_weight if total_weight > 0 else 0
        elif isinstance(merged['Vuln'].iloc[0], (int, float)):
            return merged['Vuln'].iloc[0]
    else:
        return 0

def compute_weighted_adj_index(exiobase_values, vuln_rows_clean):
    # Filter relevant rows in one go
    vuln_filtered = vuln_rows_clean[vuln_rows_clean['EXIOBASE'].isin(exiobase_values)].copy()
    # Merge on EXIOBASE / sector
    merged = vuln_filtered
    # Drop rows with missing values
    merged = merged[['Adj_ind', 'indout']].drop_duplicates().dropna().copy()
    if not merged.empty:
        if not (merged['indout'] == 0).all():
            weighted_sum = (merged['Adj_ind'] * merged['indout']).sum()
            total_weight = merged['indout'].sum()
            return weighted_sum / total_weight if total_weight > 0 else 0
        elif isinstance(merged['Adj_ind'].iloc[0], (int, float)):
            return merged['Adj_ind'].iloc[0]
    else:
        return 0
    
def get_adj_vuln(row, nace_map_df, vuln_rows_,cntry_list_ ):
    # produc the adjusted vulnerability for the info in 'row'
    # 
    cntry = row.get('ISSUER_COUNTRY')
    nace_lvl_val = row.get('nace_lvl')

    # if no country, take parameters of US
    if pd.isna(cntry) or pd.isna(nace_lvl_val) or not isinstance(cntry, str) or cntry not in cntry_list_:
        cntry = 'US' # filled up with US when country

    # Convert nace_lvl_val to int
    try:
        nace_lvl_val = int(nace_lvl_val.iloc[0]) if isinstance(nace_lvl_val, pd.Series) else int(nace_lvl_val)
    except (ValueError, TypeError, IndexError):
        return 0

    # calculate the weighted average of Vulnrability per X (MRIO prod) multiplied by weighted average of adjustment param per X
    # if the nace of the instrument is one line in vuln_rows_ just the product of Vuln X adj
    for lvl_offset in [0, -1, -2]:
        lvl = f'nace_lvl{nace_lvl_val + lvl_offset}'
        if lvl in row and lvl in nace_map_df.columns:
            nace_code = row[lvl]
            matches = nace_map_df[nace_map_df[lvl] == nace_code].copy()
            if not matches.empty and 'EXIOBASE' in matches.columns:
                exiobase_values = matches['EXIOBASE'].dropna().unique().tolist()
                vuln_rows_clean = vuln_rows_[vuln_rows_['region'] == cntry].copy()
                return compute_weighted_vuln(exiobase_values,vuln_rows_clean ) * compute_weighted_adj_index(exiobase_values, vuln_rows_clean)
            else:
                # If no match found
                return 0

        # If no match found
        return 0

def instrum_vol_alpha_def(ds_df_ ,instrmnt_df_, eco_serv_, scenario, option, nace_map_df_ , dep_type):
    # produce the list of depreciation called dpr or FLS
    # each line is an instrument
    # each value is a depreciation (adjXvulnXalpha)  

    # Filter vulnerability data for the given ecosystem service and scenario
    vuln_type_filter = f"{scenario}_{dep_type}_{option}"
    vuln_rows = ds_df_[
        (ds_df_['eco_serv'] == eco_serv_) &
        (ds_df_['Vuln_type'] == vuln_type_filter)
    ]
    cntry_list = vuln_rows['region'].unique()

    # Calculate adjusted vulnerability for each instrument
    instrmnt_df_['Vuln'] = instrmnt_df_.apply( lambda row: get_adj_vuln(row, nace_map_df_ , vuln_rows, cntry_list) , axis=1 )

    # Clean and rename vulnerability column
    cleaned_df = instrmnt_df_[[
        'PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY',
        'ISSUER_SECTOR', 'pd', 'vol' , 'debt_ratio' , 'Vuln' ] ].copy()
    cleaned_df.loc[cleaned_df['Vuln'] < 0, 'Vuln'] = 0

    new_name_vuln = f"Depr_{scenario}_{eco_serv_}"
    cleaned_df = cleaned_df.rename(columns={'Vuln': new_name_vuln})

    # Merge alpha shock data
    alpha_clean = alpha_df[
        (alpha_df['scenario'] == eco_serv_) &
        (alpha_df['Vuln_type'] == f"{scenario}_Vuln_total")&
        (alpha_df['option'] == option)
    ]

    # Step 1: Identify missing countries
    missing_countries = cleaned_df.loc[
        ~cleaned_df['ISSUER_COUNTRY'].isin(alpha_clean['ISSUER_COUNTRY'])
    ]['ISSUER_COUNTRY'].unique()

    # Step 2: Get the alpha value for the NL
    NL_alpha_value = alpha_clean.loc[alpha_clean['ISSUER_COUNTRY'] == 'NL', 'alpha'].values[0]

    # Step 3: Create a DataFrame for missing countries
    missing_alpha_clean = pd.DataFrame({
        'ISSUER_COUNTRY': missing_countries,
        'alpha': NL_alpha_value,
        'option': option
    })
    
    # Step 4: Append to alpha_data
    alpha_clean = pd.concat([alpha_clean, missing_alpha_clean], ignore_index=True)

    cleaned_df = cleaned_df.merge(
        alpha_clean[['ISSUER_COUNTRY', 'alpha']],
        on='ISSUER_COUNTRY',
        how='left')

    # multiplication of adj_Vuln and alpha = Asset_depreciation noted dpr
    cleaned_df[new_name_vuln] = cleaned_df[new_name_vuln] * cleaned_df['alpha']

    return cleaned_df[[ new_name_vuln]]

from joblib import Parallel, delayed
from itertools import product

aggreg_type = 'SR' # or 'max'
dependency_type = 'Vuln_total' # or 'DS_total'

Eco_serv_list = [ 'Soil and sediment retention','Education, scientific and research services', 'Water purification', 'Water flow regulation', 'Pollination']
# correspondance table between EXIOBASE sector and nace lvl 4,3 and 2
path = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\git_repo\\Ecosystem_ds\\data\\'
nace_map_df = pd.read_excel(path+'EXIOBASE_to_NACElvl2_tab.xlsx')

#  Run in parallel and collect DataFrames
results = Parallel(n_jobs=-1)(
    delayed(instrum_vol_alpha_def)(ds_df , instrmnt_df , eco, vuln, aggreg_type , nace_map_df, dependency_type) 
    for eco, vuln in product(Eco_serv_list, Scenario_list) )
# Concatenate all DataFrames into one
merged_df = pd.concat(results, axis=1)
final = pd.concat([ instrmnt_df[['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY', 'nace_lvl1' , 'nace_lvl3']], merged_df], axis=1)
# Save to CSV
final.to_csv('merged_SHS_instr_vulnxalpha_scenarios_'+dependency_type+'_'+aggreg_type+'.csv', index=False)

# Define functions to perform analysis
# Function to transform PD into DD
def pd_to_dd(pd):
    dd = -norm.ppf(pd)
    return dd

# Function to transform DD into PD
def dd_to_pd(dd):
    pd = norm.cdf(-dd)
    return pd

# Function to derive asset volatility from stock price volatility (vol), distance to default (dd) and debt ratio
def asset_volatility(dd, vol, debt_ratio):
    sigma = (vol / norm.cdf(dd)) * (1-debt_ratio)
    return sigma

# Function to derive modified DD
def dd_loss(dd, fls, sigma):
    dd_loss = dd -  (fls / sigma)
    return dd_loss

# Function to derive LGD
def lgd(pd, pd_calib, lgd_calib, rho):
    lgd = norm.cdf((norm.ppf(pd_calib * lgd_calib) + np.sqrt(1-rho)*norm.ppf(pd) - norm.ppf(pd_calib)) / np.sqrt(1-rho)) / pd
    return lgd

# # Function to derive spread variation
# def spread_var(duration, pd, lgd, pd_loss, lgd_loss):
#     # spread_var = pd_loss-pd # test for simplification
#     spread_var = (1/duration) * np.log((lgd*np.exp(-pd*duration) + (1-lgd)) / (lgd_loss*np.exp(-pd_loss*duration) + (1-lgd_loss)))
#     # spread_var =  np.log((lgd*np.exp(-pd) + (1-lgd)) / (lgd_loss*np.exp(-pd_loss) + (1-lgd_loss)))
#     return spread_var

# Function to evaluate risky bond price
def risky_bond_Price(duration, pd, lgd, coupon, rff):
    # rff is risk free rate constant on the periode , coupon is in % of nominal
    B_risk = 1+(coupon - rff - pd*lgd)*(1-np.exp(-(rff+pd)*duration))/(rff+pd)
    return B_risk

# Function to derive bond price variation
def bp_var(duration,pd , lgd, coupon, rff, delta_rff , delta_pd , delta_lgd ):
    bp_var = (risky_bond_Price(duration, pd + delta_pd, lgd + delta_lgd, coupon, rff + delta_rff )-risky_bond_Price(duration, pd, lgd, coupon, rff))/risky_bond_Price(duration, pd, lgd, coupon, rff)
    bp_var = bp_var.clip(lower=-1, upper=1)
    return bp_var

# Function to derive equity price variation
def ep_var(dd, dd_loss, sigma, r):
    ep_var = (np.exp(sigma*dd_loss)*norm.cdf(dd_loss) - np.exp(-r)*norm.cdf(dd_loss-sigma))/(np.exp(sigma*dd)*norm.cdf(dd) - np.exp(-r)*norm.cdf(dd-sigma)) - 1
    ep_var = ep_var.clip(lower=-1, upper=1)
    return ep_var

# Define global variables
r = 0.02 # for equity variation TBC
rho = 0.1
pd_calib = 0.0459
lgd_calib = 0.652
delta_r = 0.00
coupon = 0.02
Depr_scenario = pd.read_csv('./results/merged_vulnxalpha_scenarios_Vuln_total_SR.csv')
# pivot long 
dpr_long = Depr_scenario.melt(
    id_vars=['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY','nace_lvl1','nace_lvl3'],  # or other ID columns you want to keep
    var_name='Scenario',
    value_name='Depreciation'
)
dpr_long['Scenario'] = dpr_long['Scenario'].str.replace('Depr_', '', regex=False)
dpr_long['Eco_serv'] = dpr_long['Scenario'].str.split('_').str[-1]
dpr_long['Scenario'] = dpr_long['Scenario'].str.rsplit('_', n=1).str[0]
Depr_scenario.head(3)

# Calculate bond price and equity price variation for each scenario/ES
# scenario 
scenario_choices = dpr_long['Scenario'].drop_duplicates()
ES_choices = dpr_long['Eco_serv'].drop_duplicates()

###########################
# data cleaning for resid_mat_yr
instrmnt_df_clean = instrmnt_df
instrmnt_df_clean['resid_mat_yr'] =  instrmnt_df_clean['resid_mat_yr'].clip(upper=30) # to clip maturity below 30 to correct incoherent values (i.e 146)
# Compute the maturity mean of bonds 'F_511' and  is not null
mean_equity_a = instrmnt_df_clean.loc[(instrmnt_df_clean['INSTR_CLASS']=='F_511') & (instrmnt_df_clean['resid_mat_yr'].notnull()), 'resid_mat_yr'].mean()
# Fill missing values in 'maturity' with average only bonds
instrmnt_df_clean.loc[(instrmnt_df_clean['INSTR_CLASS']=='F_511') & (instrmnt_df_clean['resid_mat_yr'].isnull()), 'resid_mat_yr'] = mean_equity_a # small impact

# Initialize an empty DataFrames
final_table = pd.DataFrame()
for scenario, es in product(scenario_choices, ES_choices):
    # start of result calculation for one scenario
    instrmnt_df_loop = instrmnt_df_clean[['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY','ISSUER_SECTOR','nace_lvl1','resid_mat_yr', 'pd', 'vol', 'debt_ratio']]
    instrmnt_df_loop.loc[:,'Scenario']= scenario
    instrmnt_df_loop.loc[:,'Eco_serv']= es
    dpr_long_loop = dpr_long[ (dpr_long['Scenario']==scenario) & (dpr_long['Eco_serv']==es) ]
    instrmnt_df_loop = instrmnt_df_loop.merge(dpr_long_loop[['PERIOD','IDENTIFIER','Depreciation']], on=['PERIOD','IDENTIFIER'], how = 'left')
    # PD historical to RN
    # instrmnt_df_loop['pd'] = dd_to_pd(pd_to_dd(instrmnt_df_loop['pd'])+0.0*0.0) # conversion hist to RN : (correl * sharpe ratio)

    # Asset volatility
    instrmnt_df_loop['sigma'] = asset_volatility(pd_to_dd(instrmnt_df_loop['pd']), instrmnt_df_loop['vol'], instrmnt_df_loop['debt_ratio'])
    # LGD
    instrmnt_df_loop['lgd'] = lgd(pd=instrmnt_df_loop['pd'], pd_calib=pd_calib, lgd_calib=lgd_calib, rho=rho)
    # PD variation
    instrmnt_df_loop['pd_loss'] = dd_to_pd(dd=dd_loss(dd=pd_to_dd(instrmnt_df_loop['pd']), fls=-instrmnt_df_loop['Depreciation'] , sigma=instrmnt_df_loop['sigma'])) 
    # LGD_loss
    instrmnt_df_loop['lgd_loss'] = lgd(pd=instrmnt_df_loop['pd_loss'], pd_calib=pd_calib, lgd_calib=lgd_calib, rho=rho)
    # Bond price variation
    instrmnt_df_loop['bp_var'] = np.where(
        instrmnt_df_loop['INSTR_CLASS']=='F_511',
        np.nan, 
        bp_var( instrmnt_df_loop['resid_mat_yr'] , instrmnt_df_loop['pd'] , instrmnt_df_loop['lgd'], coupon , r , delta_r , instrmnt_df_loop['pd_loss'] , instrmnt_df_loop['lgd_loss'] ) )
    # Equity price variation
    instrmnt_df_loop['ep_var'] = np.where(
        instrmnt_df_loop['INSTR_CLASS']!='F_511',
        np.nan, 
        ep_var(dd=pd_to_dd(instrmnt_df_loop['pd']), dd_loss=pd_to_dd(instrmnt_df_loop['pd_loss']), sigma=instrmnt_df_loop['sigma'], r=r))
    # Define price variation as bp_var for bonds and ep_var for equity
    instrmnt_df_loop['p_var'] = np.where(
        instrmnt_df_loop['ep_var'].notna(),
        instrmnt_df_loop['ep_var'],
        instrmnt_df_loop['bp_var'])
    instrmnt_df_loop['Security_type'] = np.where(
        instrmnt_df_loop['ep_var'].notna(),
        'Equity',
        'Bonds')
    final_table = pd.concat([final_table, instrmnt_df_loop.reset_index()], ignore_index=True)

# Define the common keys for merging instrument and depreciation values
merge_keys = ['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY', 'ISSUER_SECTOR' , 'Scenario', 'Eco_serv']
# Select only the necessary columns from instrmnt_df
instrmnt_df_subset = final_table[merge_keys + ['p_var','Security_type','resid_mat_yr','nace_lvl1']]

###########################
# Perform the merge
instrmnt_df_clean = pd.merge(dpr_long, instrmnt_df_subset, on=merge_keys, how='left')
instrmnt_df_clean.sort_values(by='p_var', ascending=False).head(3)
instrmnt_df_clean
# instrmnt_df_clean.to_csv('analysis_instr_clean.csv', index=False)

# Merge with SHS-S holder x instrument to obtain exposure
shs_holder_instrmnt_df = pd.read_csv('H:/Documents/SHS/prepped/F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv')
# merge
shs_results = instrmnt_df_clean.merge(shs_holder_instrmnt_df, on= ['PERIOD', 'IDENTIFIER'], how='left')
# Create VALUE_LOSS
shs_results["VALUE_LOSS"] = shs_results["p_var"] * shs_results["OBS_VALUE"]
# Keep relevant columns: 4 types of info (holder , security , price info , scenario_looked)
shs_results = shs_results[["HOLDER_SECTOR", "HOLDER_AREA",'Security_type','nace_lvl1', 'ISSUER_COUNTRY' , 'VALUE_LOSS', "OBS_VALUE", "Eco_serv", "Scenario"]] 

# Aggregate by sum
shs_results = shs_results.groupby(["HOLDER_SECTOR", "HOLDER_AREA", 'Security_type','nace_lvl1', 'ISSUER_COUNTRY', "Eco_serv", "Scenario"], as_index=False).sum()

# Write results to csv
shs_results.to_csv('./shs_2024-Q4_results.csv', index=False)

# Graphs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#### FOR ONE SCENARIO / ES ####
# Set your filter values
ES = 'Water flow regulation' # 'Water supply', 'Rainfall pattern regulation' , 'Water purification', 'Pollination' ,'Water flow regulation'
scenario = '1_World_shock_10perc_02_GOVonNFC' # '1_World_shock_10perc_02_GOVonNFC' , '0_World_shock_10perc_02_GOVonNFC', '0_World_shock_10perc_02_GOVonNFC', '1_EUshock_3perc_08_GOVonNFC', '1_EUshock_3perc_08_GOVonNFC' , '1_World_shock_10perc_02_GOVonNFC' , '1_World_shock_3perc_02_GOVonNFC'
# option 'SR' or 'max' and Vuln_total or DS_total decided by Depr_scenario = pd.read_csv('./merged_vulnxalpha_scenarios_Vuln_total_max.csv')
dimensionX = 'nace_lvl1' # 'Security_type' # 'HOLDER_AREA' # 
dimensionY = 'HOLDER_SECTOR' # 'Security_type' #
# Create the DataFrame from the provided data
df = pd.DataFrame(shs_results[(shs_results['Eco_serv']==ES) & (shs_results['Scenario']==scenario )][[dimensionX, dimensionY , 'VALUE_LOSS', 'OBS_VALUE']])

# Aggregate VALUE_LOSS and OBS_VALUE by Eco_serv and HOLDER_SECTOR
aggregated = df.groupby([dimensionX, dimensionY ], as_index=False).agg({
    'VALUE_LOSS': 'sum',
    'OBS_VALUE': 'sum'})
aggregated['Perc_LOSS'] = aggregated['VALUE_LOSS'] / aggregated['OBS_VALUE']

### Euro amount or percentage choice ###
choice = ['VALUE_LOSS', 'eur' , 2] # ['Perc_LOSS', '%' , 1] #['VALUE_LOSS', 'eur' , 2] # ['OBS_VALUE', 'eur' , 2]

# Pivot the table
pivot_table = aggregated.pivot(index=dimensionX, columns=dimensionY, values=choice[0])
# Plot heatmap
# sort descending for the first columns X axis
pivot_table_percent = pivot_table.sort_values(by=pivot_table.columns[0], ascending=True)
# Create annotation labels as percentage strings
if choice[2]==1:
    annotations = pivot_table_percent.map(lambda x: f"{x * 100 :.2f}%" if pd.notnull(x) else "")
else:
    annotations = pivot_table_percent.map(lambda x: f"{x / 1_000_000_000:.2f}b" if pd.notnull(x) else "")

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table_percent, annot=annotations, fmt="", cmap="Reds_r", linewidths=0.5)
plt.title("Heatmap of losses in "+choice[1] +" by " + dimensionX + ' and '+ dimensionY)
plt.ylabel(dimensionX)
plt.xlabel(dimensionY)
plt.tight_layout()
plt.show()


