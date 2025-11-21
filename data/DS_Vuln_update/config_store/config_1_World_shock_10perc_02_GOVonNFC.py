"""
Scenario: World shock 10% with Gov/NFC ratio 0.2
WITH government/financial sector vulnerability calculation

Created on 15 sept 2025
Based on ENCORE and EXIOBASE 2022 update

@author: DNB FS-IFA NC5452 (sebastien gallet)
"""
import pandas as pd

# =============================================================================
# SCENARIO-SPECIFIC PARAMETERS ONLY
# All data paths are centralized in nature_analysis/config.py
# =============================================================================

# ENCORE rating mapping options (scenario-specific)
rating_mapping_linear = {'ND': 0, 'VL': 0.2, 'L': 0.4, 'M': 0.6, 'H': 0.8, 'VH': 1}
rating_mapping_exp = {'ND': 0, 'VL': 0.06, 'L': 0.13, 'M': 0.25, 'H': 0.5, 'VH': 1}
rating_mapping_S = {'ND': 0, 'VL': 0.06, 'L': 0.2, 'M': 0.8, 'H': 0.94, 'VH': 1}

# Selected rating mapping for this scenario
rating_mapping = rating_mapping_linear

# Production shock by region (10% global shock)
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
        'Eastern Europe (non-EU)'
    ],
    "Production shock": [
        -0.1,  # 10% shock
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1,
        -0.1
    ]
}
data_shock = pd.DataFrame(data_shock)

# Government/NFC ratio in financial portfolio
ratio_Gov_on_NFCpGov = 0.2

# Vulnerability calculation activation flags
activation_gov_vuln = 1  # Activate alternative gov vulnerability calculation
activation_fin_vuln = 1  # Activate alternative financial vulnerability calculation
