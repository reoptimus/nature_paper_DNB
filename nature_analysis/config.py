"""
Configuration settings for SHS Nature Analysis
"""
from pathlib import Path

# File paths
BASE_PATH = Path('I:/FS/FS/Statsp/000-Beleidsmedewerkers/Sebastien Gallet/Biodiv/OS-2025')
DATA_PATH = BASE_PATH / 'git_repo/nature_paper_DNB/data'
VULN_PATH = BASE_PATH / 'DS_Vuln_update/Vuln_final_store'
ANALYSIS_PATH = BASE_PATH / 'analysis/output_data'
RESULTS_PATH = Path('./results')

# Input files in secured environment
# SHS instrument data
SHS_INSTRUMENT_FILE = 'G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/SHS/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'
# AnaCredit instrument data
ANACREDIT_INSTRUMENT_FILE = 'G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/anacredit_NL/anacredit_instrmnt_nature_prepped.csv'
VULN_FILE = 'Vuln_final_03_11_2025.csv'
ALPHA_FILE = 'Alpha_final_03_11_2025.xlsx'
X_FILE = BASE_PATH / 'downloaded_data/EXIOBASE 3/IOT_2022_ixi/IOT_2022_ixi/x.csv'
NACE_MAP_FILE = DATA_PATH / 'nace_0d_map.xlsx'
EXIOBASE_NACE_MAP = DATA_PATH / 'EXIOBASE_to_NACElvl2_tab.xlsx'
AREA_MAP_FILE = DATA_PATH / 'regions_ISO2_continent_area.csv'
SHS_HOLDER_FILE = 'H:/Documents/SHS/prepped/F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv'

# Analysis parameters
AGGREG_TYPE = 'SR'  # or 'max'
DEPENDENCY_TYPE = 'Vuln_total'  # or 'DS_total'
ECO_SERVICES = [
    'Soil and sediment retention',
    'Education, scientific and research services',
    'Water purification',
    'Water flow regulation',
    'Pollination'
]

# Country lists
COUNTRY_LIST = ['NL', 'AT', 'BE', 'DE', 'ES', 'FI', 'FR', 'GR', 'HR', 'IT', 
                'PL', 'PT', 'US', 'JP', 'CN', 'CA']

# Financial parameters
RISK_FREE_RATE = 0.02
CORRELATION_RHO = 0.1
PD_CALIB = 0.0459
LGD_CALIB = 0.652
DELTA_RATE = 0.00
COUPON = 0.02
MAX_MATURITY = 30  # years

# Visualization defaults
DEFAULT_COLORMAP = 'BrBG'
FIGURE_SIZE = (10, 6)
