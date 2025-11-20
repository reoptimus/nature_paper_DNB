"""
Configuration settings for SHS Nature Analysis
"""
from pathlib import Path

# File paths
BASE_PATH = Path('I:/FS/FS/Statsp/000-Beleidsmedewerkers/Sebastien Gallet/Biodiv/OS-2025')
DATA_PATH = BASE_PATH / 'git_repo/nature_paper_DNB/data'
VULN_config_PATH = BASE_PATH / 'DS_Vuln_update/config_store'
VULN_final_PATH = BASE_PATH / 'DS_Vuln_update/Vuln_final_store'
VULN_PATH = VULN_final_PATH  # Alias for backwards compatibility
ANALYSIS_PATH = BASE_PATH / 'analysis/output_data'

# Input files in secured environment
# SHS instrument data
SECURED_DRIVE_PATH = Path('G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/')
SHS_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'SHS/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'
SHS_HOLDER_FILE = SECURED_DRIVE_PATH / 'SHS/F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv'
# AnaCredit instrument data
ANACREDIT_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'anacredit_NL/anacredit_df_2024-12-31.csv'
# results (also in secured env.)
RESULTS_PATH = SECURED_DRIVE_PATH / 'results/'

# File calculated based on ENCORE and EXIOBASE (used by main pipeline)
# These are the OUTPUT files from vulnerability generation
VULN_FILE = 'Vuln_final_03_11_2025.csv'
ALPHA_FILE = 'Alpha_final_03_11_2025.xlsx'
X_FILE = BASE_PATH / 'downloaded_data/EXIOBASE 3/IOT_2022_ixi/IOT_2022_ixi/x.csv'

# =============================================================================
# VULNERABILITY GENERATION PARAMETERS
# (Optional - only needed if regenerating vulnerability files from scratch)
# =============================================================================

# Input data sources for vulnerability generation
# ENCORE: Ecosystem service dependency ratings
ENCORE_FILE = BASE_PATH / 'downloaded_data/ENCORE/06. Dependency mat ratings.csv'
ENCORE_RATING_MAPPING = {
    'Very High': 4,
    'High': 3,
    'Medium': 2,
    'Low': 1,
    'Very Low': 0.5
}

# EXIOBASE: Multi-regional input-output data
EXIOBASE_PATH = BASE_PATH / 'downloaded_data/EXIOBASE 3/IOT_2022_ixi/IOT_2022_ixi'
EXIOBASE_A_MATRIX = EXIOBASE_PATH / 'A.csv'
EXIOBASE_Z_MATRIX = EXIOBASE_PATH / 'Z.csv'
EXIOBASE_X_VECTOR = EXIOBASE_PATH / 'x.csv'

# ISIC to NACE mapping
ISIC_NACE_MAPPING = BASE_PATH / 'downloaded_data/ENCORE/14. EXIOBASE NACE ISIC crosswalk.csv'

# ND-GAIN: Nature degradation vulnerability indices
ND_GAIN_PATH = BASE_PATH / 'downloaded_data/Nature degradation/ND_GAIN index/vulnerability'
ISO_CODES_PATH = BASE_PATH / 'downloaded_data/Misc_tables'

# Additional vulnerability generation parameters
ADJ_IND_FILE = 'Adj_ind_per_NACE.xlsx'  # Adjustment indicators per NACE sector

# Vulnerability generation settings
ACTIVATION_GOV_VULN = 1  # 1 to activate government sector vulnerability calculation
ACTIVATION_FIN_VULN = 1  # 1 to activate financial sector vulnerability calculation
RATIO_GOV_ON_NFC = 0.5  # Ratio of government to (non-financial corporate + government)

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
PD_CALIB = 0.0459
LGD_CALIB = 0.652
DELTA_RATE = 0.00
COUPON = 0.02
MAX_MATURITY = 30  # years

# Visualization defaults
DEFAULT_COLORMAP = 'BrBG'
FIGURE_SIZE = (10, 6)
