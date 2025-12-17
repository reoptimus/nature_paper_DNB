#!/usr/bin/env python3
"""
Example script demonstrating package usage

NOTE: To use this package, ensure you have the required dependencies:
    pip install pandas numpy scipy matplotlib seaborn joblib openpyxl

The package is now organized as 'nature_analysis'.
"""

##################################
## initialisation C:/Users/NC5452/Documents/Scripts/activat
################################
# connection issu to azure solved by running following lines in PowerShell...
# az config set core.encrypt_token_cache=false  # 1) Temporarily disable file-cache encryption to allow clearing
# az account clear  # 2) Clear account state (this uses the cache)
# az config set core.enable_broker_on_windows=false  # 3) Optionally disable the broker to force browser/device-code login
# az login --use-device-code  # 4) Re-login (use device-code if the browser flow is stubborn)

import pandas as pd
import numpy as np
from pathlib import Path
from itertools import product
import logging
import importlib

from nature_analysis import (
    pipeline,
    vulnerability,
    config,
    data_loader,
    visualization
)
importlib.reload(pipeline)
importlib.reload(vulnerability)
importlib.reload(data_loader)
importlib.reload(config)

def case_0_Vulnerability_DS_generator():
    import importlib
    import nature_analysis
    shapes = nature_analysis.regenerate_vulnerability_files()

def case_1_production_losses_EXIOBASE_calculation():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Merge vulnerability data and Alpha to generate Delta Industrial production (delta_indout)...")
    data_prod_losses = pipeline.prepare_production_loss_analysis()

    # graphic
    list_eco_system = data_prod_losses['eco_serv'].unique()
    eco_service = 'Water flow regulation'
    list_scenario = data_prod_losses['Vuln_type'].unique()
    scenario = list_scenario[5]
    full_list_country = data_prod_losses['region'].unique()
    retained_list_region = ['AT', 'BE', 'DE', 'DK', 'ES', 'FR',
       'GR', 'IT', 'NL', 'GB', 'US', 'JP', 'CN']
   
    plt = visualization.plot_loss_heatmap_by_region(data_prod_losses,
                                   eco_service,
                                   scenario,
                                   'nace_lvl1',
                                   ['FR','NL, '],
                                   'percentage',
                                   None)
    plt.show()

def case_2_market_lossess_SHS_calculation():
    """Custom analysis workflow."""
    print("\nExample 5: Depreciation calculation and write")
    print("=" * 60)

    from nature_analysis.pipeline import SHSAnalysisPipeline
    pipeline_SHS = SHSAnalysisPipeline()
    pipeline_SHS.load_all_data()
    pipeline_SHS.instrmnt_df

    # Calculate depreciation for this specific case
    SHS_losses_df = pipeline_SHS.calculate_financial_impacts()

    # save results for market losses analysis
    SHS_losses_df.to_excel(
    config.RESULTS_PATH / "SHS_Losses_all_scenario_ecosystem.xlsx",
    index=False )

    # to aggregate result at lvl1 level for graph and presentation
    data_loader.aggregate_shs_losses(
        config.RESULTS_PATH / "SHS_Losses_all_scenario_ecosystem.xlsx",
        config.RESULTS_PATH / "SHS_Losses_aggregated_lvl1.xlsx")

def case_3_prudential_lossess_banks_CET1_calculation():
    # CET1 variation due to loans EL and RWA -> based on pd variations
    # import COREP data to re-evaluate CET1 position after pd degradation
    from nature_analysis.pipeline import AnaCreditAnalysisPipeline
    pipeline_anacredit = AnaCreditAnalysisPipeline()
    pipeline_anacredit.load_all_data()
    # pipeline_anacredit.instrmnt_df

    # Calculate depreciation for this specific case
    Anacred_delta_PD_df = pipeline_anacredit.calculate_delta_CET1()

def case_4_prudential_lossess_insurances_SCR_calculation():  
    # SCR variation due to market valuation of assets -> based on pd variations
    # import ARS S2 data BS and SCR to re-evaluate SCR position after pd degradation
    # S2_ARS_data_BS = data_loader.load_S2_ARS_data_BS()
    S2_ARS_data_SCR_s2 = data_loader.load_S2_ARS_data_SCR()
    S2_ARS_data_dA_market_s2 = data_loader.load_S2_ARS_data_dA()
    S2_ARS_data_clean = S2_ARS_data_SCR_s2.merge(S2_ARS_data_dA_market_s2 , on = ['relatienummer', 'LEI' ,'RIAD'], how = 'inner')
    S2_ARS_data_clean['delta_SCR_cof'] = (-1) * S2_ARS_data_clean['Market risk SCR'] / ( S2_ARS_data_clean['basic SCR'] * S2_ARS_data_clean['dA_s2'] ) 
    S2_ARS_data_clean['LEI','delta_SCR_cof']
   
    # import market losses per insurance
    SHS_GEC_data = data_loader.load_SHS_GEC_data()
    SHS_GEC_data.columns
    # calcul of losses based on nace, ESA_2010_INSTRUMENT_CLASS, ...
    
    # calculate SCR variation
    


if __name__ == "__main__":
    import sys

    print("Nature Analysis Package - Usage Examples")
    print("=" * 60)
    print("\nNOTE: This requires renaming the directory or setting up PYTHONPATH")
    print("See script header for details.\n")

    try:
        # Try to import the package
        import nature_analysis
        print(f"✓ Package imported successfully (version {nature_analysis.__version__})")
        print("\nChoose an example to run:")
        print("1. Simple usage")
        print("2. Class usage")
        print("3. Step-by-step execution")
        print("4. Module access (no data needed)")
        print("5. Custom analysis")

    except ImportError as e:
        print(f"✗ Cannot import package: {e}")
        print("\nPlease ensure the package is properly installed.")
        print("From the repository root, run: pip install -e .")
        sys.exit(1)
