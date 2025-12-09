"""
Configuration settings for SHS Nature Analysis
"""
from pathlib import Path

# File paths
BASE_PATH = Path('I:/FS/FS/Statsp/000-Beleidsmedewerkers/Sebastien Gallet/Biodiv/OS-2025')
DATA_PATH = BASE_PATH / 'git_repo/nature_paper_DNB/data'
DS_VULN_UPDATE_PATH = DATA_PATH / 'DS_Vuln_update'
VULN_config_PATH = DS_VULN_UPDATE_PATH / 'config_store'
VULN_final_PATH = DS_VULN_UPDATE_PATH / 'Vuln_final_store'
VULN_PATH = VULN_final_PATH  # Alias for backwards compatibility
ANALYSIS_PATH = BASE_PATH / 'analysis/output_data'

####################################
# Input files in secured environment
# SHS instrument data
SECURED_DRIVE_PATH = Path('G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/')
SHS_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'SHS/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'
SHS_HOLDER_FILE = SECURED_DRIVE_PATH / 'SHS/F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv'
# AnaCredit instrument data
ANACREDIT_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'anacredit_NL/anacredit_df_2024-12-31.csv'
# COREP
COREP_FILE = SECURED_DRIVE_PATH / 'COREP/corep_extract_date_2024_12_31.csv'
# ARS Solvency 2
S2_ARS_FILE = SECURED_DRIVE_PATH / 'ARS_solva2/S2ARS_S02_01_31122024.csv'
# results (also in secured env.)
RESULTS_PATH = SECURED_DRIVE_PATH / 'results'
###################################

# File calculated based on ENCORE and EXIOBASE (used by main pipeline)
# These are the OUTPUT files from vulnerability generation
VULN_FILE = 'Final_Vuln_file.csv'
ALPHA_FILE = 'Final_alpha_file.xlsx'

# =============================================================================
# VULNERABILITY GENERATION PARAMETERS
# (Optional - only needed if regenerating vulnerability files from scratch)
# =============================================================================

# Input data sources for vulnerability generation
# ENCORE: Ecosystem service dependency ratings
ENCORE_PATH = 'downloaded_data/ENCORE/ENCORE files October 2024_072025'
ENCORE_FILE = BASE_PATH / ENCORE_PATH / '06. Dependency mat ratings.csv'
# ISIC to NACE mapping
ISIC_NACE_MAPPING = BASE_PATH / ENCORE_PATH / '14. EXIOBASE NACE ISIC crosswalk.csv'

# EXIOBASE: Multi-regional input-output data
EXIOBASE_PATH = BASE_PATH / 'downloaded_data/EXIOBASE 3/IOT_2022_ixi/IOT_2022_ixi'
EXIOBASE_A_MATRIX = EXIOBASE_PATH / 'A.csv'
EXIOBASE_Z_MATRIX = EXIOBASE_PATH / 'Z.csv'
EXIOBASE_X_VECTOR = EXIOBASE_PATH / 'x.csv'

# Nature Index: Nature degradation vulnerability indices (ND-GAIN)
NATURE_INDEX_PATH = BASE_PATH / 'downloaded_data/Nature degradation/ND_GAIN index/vulnerability'
ISO_CODES_PATH = BASE_PATH / 'downloaded_data/Misc_tables'

# Additional vulnerability generation parameters
ADJ_IND_FILE = 'ROE_ROA_debt_ratio per NACE lvl1/Adj_ind_by_industry.xlsx'  # Adjustment indicators per NACE sector
AREA_COUNTRY_CODE_FILE = 'regions_ISO2_continent_area.csv'  # ISO2 to area/continent mapping

# =============================================================================
# sector and country correspondance mapping
NACE_MAP_FILE = DATA_PATH / 'nace_0d_map.xlsx'
EXIOBASE_NACE_MAP = DATA_PATH / 'EXIOBASE_to_NACElvl2_tab.xlsx'
AREA_MAP_FILE = DATA_PATH / 'regions_ISO2_continent_area.csv'

# extra info on equity price volatility and debt_ratio per sector nace lvl2
VOL_FILE = DATA_PATH / 'volatility_per_nace_lvl2.xlsx'
DEBT_RATIO_FILE = DATA_PATH / 'Debt_ratio_per_nace_lvl2.xlsx'

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
PD_CALIB = 0.0459 # LGD model parameter from Frye and Jacobs approximation function
LGD_CALIB = 0.652 # LGD model parameter from Frye and Jacobs approximation function
DELTA_RATE = 0.00 # for an interest curve shift
COUPON = 0.02 # assumption for the bond price variation
MAX_MATURITY = 30  # maturity max in years for data cleaning

# model options
RWA_calc_option = 'flat' # 'flat' or 'base'  ; regulation function f for PD drop after a maximum in the regulation
EL_calc_option = 'no' # 'yes' or 'no'  ; recalculation of LGD after PD variation (base on Frye and Jacobs approximation function, reference in EDSI paper)

# Visualization defaults
DEFAULT_COLORMAP = 'BrBG'
FIGURE_SIZE = (10, 6)
