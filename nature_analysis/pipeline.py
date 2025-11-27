"""
Main pipeline for SHS Nature Analysis
Orchestrates the complete analysis workflow
"""
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import product
import logging
import importlib

from . import config
from . import data_loader
from . import vulnerability
from . import financial
from . import visualization

from nature_analysis import (
    pipeline,
    vulnerability,
    config,
    data_loader,
     financial
)
importlib.reload(pipeline)
importlib.reload(vulnerability)
importlib.reload(data_loader)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def prepare_production_loss_analysis() -> pd.DataFrame:
    """
    Prepare and analyze production losses.
    
    Returns merged dataframe with production loss calculations.
    """
    logger.info("Loading vulnerability data...")
    vuln_df = data_loader.load_vulnerability_data()
    
    logger.info("Loading alpha shock data...")
    alpha_df = data_loader.load_alpha_data()

    logger.info("Loading NACE mappings...")
    nace_map = data_loader.load_nace_mapping(mapping_type='simple')
    
    # Prepare merged data with alpha
    results = data_loader.prepare_vulnerability_with_alpha(vuln_df, alpha_df)

    # merge to ad NACE lvl1
    # Step 1: Make sure the codes are in the same format (integers)
    results_clean = results[ pd.to_numeric(results['NACE Code'], errors='coerce').notnull() ]
    results_clean['NACE Code'] = results_clean['NACE Code'].astype(int)
    nace_map['nace_2d_code'] = nace_map['nace_2d_code'].astype(int)

    # Step 2: Merge on the code
    results_merged = results_clean.merge(
        nace_map[['nace_2d_code', 'nace_0d_code']], 
        left_on='NACE Code', 
        right_on='nace_2d_code',
        how='left'
    )

    # Step 3: Drop helper column if you don’t need it
    results_merged = results_merged.rename(columns={'nace_0d_code': 'nace_lvl1'})
    results_merged = results_merged.drop(columns=['nace_2d_code'])
    # print(results_merged.head())

    return results_merged


class SHSAnalysisPipeline:
    """Main pipeline for running SHS nature analysis."""
    
    def __init__(self):
        self.instrmnt_df = None
        self.vuln_df = None
        self.alpha_df = None
        self.nace_map = None
        self.scenarios = None
        self.eco_services = None
        
    def load_all_data(self):
        """Load all required data files."""
        logger.info("Loading instrument data...")
        self.instrmnt_df = data_loader.load_SHS_data()
        
        logger.info("Loading vulnerability data...")
        self.vuln_df = data_loader.load_vulnerability_data()
        
        logger.info("Loading alpha shock data...")
        self.alpha_df = data_loader.load_alpha_data()
        
        logger.info("Loading NACE mappings...")
        self.nace_map = data_loader.load_nace_mapping(mapping_type='detailed')
        
        # Extract scenario information
        self.scenarios, self.eco_services = data_loader.extract_scenario_info(self.vuln_df)
        
        logger.info(f"Loaded {len(self.scenarios)} scenarios and {len(self.eco_services)} ecosystem services")
        
        return
    
    def calculate_financial_impacts(self) -> pd.DataFrame:
        """
        Calculate financial impacts (PD, LGD, price variations) for all scenarios.
        
        Args:
            depreciation_df: DataFrame with depreciation columns
        
        Returns:
            DataFrame with financial impact calculations
        """
        logger.info("Calculating financial impacts...")
        
        """
        Calculate delta_PD for all instruments across all scenarios.
        
        Returns DataFrame with delta PDs columns for each scenario/ES combination.
        """
        
        # Use configured eco services or all available
        eco_services = config.ECO_SERVICES if hasattr(config, 'ECO_SERVICES') else self.eco_services

        logger.info("Calculating instrument depreciations (takes 20 to 50 min)...")
        depreciation_df = vulnerability.calculate_all_deltaPD_SHS(
            self.vuln_df,
            self.instrmnt_df,
            self.alpha_df,
            eco_services,
            self.scenarios,
            self.nace_map,
            config.AGGREG_TYPE,
            config.DEPENDENCY_TYPE,
            n_jobs=-1
        )
        # pipeline_SHS. = self
        # depreciation_df = vulnerability.calculate_all_deltaPD_SHS(
        #     pipeline_SHS.vuln_df,
        #     pipeline_SHS.instrmnt_df,
        #     pipeline_SHS.alpha_df,
        #     eco_services,
        #     pipeline_SHS.scenarios,
        #     pipeline_SHS.nace_map,
        #     config.AGGREG_TYPE,
        #     config.DEPENDENCY_TYPE,
        #     n_jobs=-1
        # )
        
        # Clean maturity data
        instrmnt_clean = data_loader.clean_instrument_maturity(depreciation_df)
        # instrmnt_clean = data_loader.clean_instrument_maturity(pipeline_SHS.instrmnt_df)
        
        # Load holder-instrument data
        shs_holder_df = data_loader.load_shs_holder_data()

        # Calculate impacts for each holder/scenario/ES
        shs_results = []
        final_results_SHS = pd.DataFrame()
        for scenario, es in product(depreciation_df['scenario'].unique(), depreciation_df['eco_service'].unique()): # scenario = '1_World_shock_10perc_02_GOVonNFC' ; es = 'Water purification'
            logger.info(f"Processing scenario: {scenario}, ES: {es}")
            
            # Prepare data for this scenario
            instrmnt_loop = instrmnt_clean[
                (instrmnt_clean['scenario'] == scenario) &
                (instrmnt_clean['eco_service'] == es)
            ]

            # Calculate financial impacts
            financial_impacts = financial.calculate_prices_impacts(instrmnt_loop)
            # financial_impacts[financial_impacts['Security_type']!='Equity']

            # Select relevant columns from financial impacts
            merge_cols = ['IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY',
                        'nace_lvl4', 'nace_lvl2', 'nace_lvl', 'scenario', 'eco_service']
            impact_subset = financial_impacts[merge_cols + ['p_var', 'Security_type']]
            # financial_impacts.columns
            # Merge with holder data
            shs_results = impact_subset.merge(
                shs_holder_df,
                on=['IDENTIFIER'],
                how='left'
            )
            
            # Calculate value loss
            shs_results['VALUE_LOSS'] = shs_results['p_var'] * shs_results['OBS_VALUE']
            
            # Select and aggregate
            result_cols = ['HOLDER_SECTOR', 'HOLDER_AREA',
                            'INSTR_CLASS','Security_type', 'ISSUER_COUNTRY',
                            'nace_lvl2', 'nace_lvl', 'scenario', 'eco_service']         
            
            shs_results = shs_results[result_cols+['VALUE_LOSS','OBS_VALUE'] ].groupby(result_cols,  as_index=False).sum()
            shs_results['loss_perc'] = shs_results['VALUE_LOSS']/shs_results['OBS_VALUE']
            # aggregation of new results
            final_results_SHS = pd.concat( [shs_results, final_results_SHS] , ignore_index=True)
        
        # merge NACE lvl1 : step 1, loading
        logger.info("Loading NACE mappings...")
        nace_map = data_loader.load_nace_mapping(mapping_type='simple')
        # Step 2: Merge on the code
        results_merged = final_results_SHS.merge(
        nace_map[['nace_2d_code', 'nace_0d_code']], 
        left_on='nace_lvl2', 
        right_on='nace_2d_code',
        how='left'
        )
        # Step 3: Drop helper column if you don’t need it
        results_merged = results_merged.rename(columns={'nace_0d_code': 'nace_lvl1'})
        results_merged = results_merged.drop(columns=['nace_2d_code'])
        return results_merged
    

class AnaCreditAnalysisPipeline:
    """Pipeline for running AnaCredit nature analysis."""

    def __init__(self):
        self.instrmnt_df = None
        self.vuln_df = None
        self.alpha_df = None
        self.nace_map = None
        self.scenarios = None
        self.eco_services = None

    def load_all_data(self):
        """Load all required data files for AnaCredit analysis."""

        logger.info("Loading AnaCredit instrument data...")
        self.instrmnt_df = data_loader.load_Anacredit_data()
        # rename of columns for better correspondance between SHS and AnaCredit code
        
        list_names_col = ['PERIOD','Credtr_IDENTIFIER', 'Dbtr_IDENTIFIER','ISSUER_SECTOR','nace_lvl4','ISSUER_COUNTRY','pd' , 'IDENTIFIER_B' , 'IDENTIFIER' , 'to_delete1' , 'to_delete2' , 'incept_AMOUNT' , 'OUTSTANDING_AMOUNT' , 'Credtr_SECTOR', 'nace_lvl2','INSTR_CLASS','vol' , 'debt_ratio']
        self.instrmnt_df.columns = list_names_col

        logger.info("Loading vulnerability data...")
        self.vuln_df = data_loader.load_vulnerability_data()

        logger.info("Loading alpha shock data...")
        self.alpha_df = data_loader.load_alpha_data()

        logger.info("Loading NACE mappings...")
        self.nace_map = data_loader.load_nace_mapping(mapping_type='detailed')

        # Extract scenario information
        self.scenarios, self.eco_services = data_loader.extract_scenario_info(self.vuln_df)

        logger.info(f"Loaded {len(self.scenarios)} scenarios and {len(self.eco_services)} ecosystem services")

        return

    def calculate_delta_CET1(self) -> pd.DataFrame:
        """
        Calculate depreciations for all AnaCredit instruments across all scenarios.

        Returns DataFrame with depreciation columns for each scenario/ES combination.
        """
        logger.info("Calculating AnaCredit instrument depreciations...")
        # self = pipeline_anacredit
        deltaEL_RWA_results = vulnerability.calculate_PD_EL_RWA_variation(self)

        #################################
        # to be passed to vulnerability.py
        # aggregation per creditor
        # Select relevant columns
        Aggreg_deltaEL_RWA_tabl = deltaEL_RWA_results[ # 'nace_lvl2', 'nace_lvl', 
            ['Credtr_IDENTIFIER', 'ISSUER_COUNTRY',
            'scenario', 'eco_service', 'delta_EL', 'delta_rwa', 'OUTSTANDING_AMOUNT']
        ]
        # Group by and sum
        Aggreg_deltaEL_RWA_tabl = (
            Aggreg_deltaEL_RWA_tabl
            .groupby(['Credtr_IDENTIFIER', # 'nace_lvl2', 'nace_lvl',
                    'ISSUER_COUNTRY', 'scenario', 'eco_service'], as_index=False)
            .sum()
        )
        #################################
        # merge with COREP
        # COREP load
        COREP_tab = data_loader.load_COREP_data()
        # Filter rows where same RIAD code for INDividual and CONsolidated institution, then keep conso == 'ind'
        corep_filtered = COREP_tab[COREP_tab['consolidation_code'] == 'ind'][['institution_name','riad_code','CET1','RWA','cet1_ratio']]
        # Merge on 'riad_code'
        merged_df = pd.merge(
            Aggreg_deltaEL_RWA_tabl,
            corep_filtered,
            left_on= 'Credtr_IDENTIFIER',
            right_on= "riad_code",
            how="left"   # or "inner" depending on whether you want to keep only matches
        )
        CET1_results = merged_df.drop(columns=["riad_code"])
        CET1_results = CET1_results.dropna(subset=["institution_name"])
        # delta_CET1 calculation
        CET1_results['delta_CET1_ratio'] = (CET1_results['CET1'] - CET1_results['delta_EL']) / (CET1_results['RWA'] + CET1_results['delta_rwa']) - CET1_results['cet1_ratio']

        # result storage
        # output_file = (config.RESULTS_PATH /
        #               f'merged_AnaCredit_instr_vulnxalpha_scenarios_{config.DEPENDENCY_TYPE}_{config.AGGREG_TYPE}.csv')
        # all_delta_PD_df.to_csv(output_file, index=False)
        # logger.info(f"Saved AnaCredit depreciation data to {output_file}")

        return CET1_results

    def calculate_financial_impacts(self, depreciation_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate financial impacts for AnaCredit instruments.

        Args:
            depreciation_df: DataFrame with depreciation columns

        Returns:
            DataFrame with financial impact calculations
        """
        logger.info("Calculating AnaCredit financial impacts...")

        # Reshape depreciation data to long format
        id_cols = ['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY',
                   'nace_lvl1', 'nace_lvl3']

        dpr_long = depreciation_df.melt(
            id_vars=id_cols,
            var_name='Scenario',
            value_name='Depreciation'
        )

        # Clean scenario names
        dpr_long['Scenario'] = dpr_long['Scenario'].str.replace('Depr_', '', regex=False)
        dpr_long['Eco_serv'] = dpr_long['Scenario'].str.split('_').str[-1]
        dpr_long['Scenario'] = dpr_long['Scenario'].str.rsplit('_', n=1).str[0]

        # Clean maturity data
        instrmnt_clean = data_loader.clean_instrument_maturity(self.instrmnt_df)

        # Get unique scenario/ES combinations
        scenario_choices = dpr_long['Scenario'].unique()
        es_choices = dpr_long['Eco_serv'].unique()

        # Calculate impacts for each scenario/ES
        results_list = []

        for scenario, es in product(scenario_choices, es_choices):
            logger.info(f"Processing AnaCredit scenario: {scenario}, ES: {es}")

            # Prepare data for this scenario
            instrmnt_loop = instrmnt_clean[[
                'PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY',
                'ISSUER_SECTOR', 'nace_lvl1', 'resid_mat_yr', 'pd', 'vol', 'debt_ratio'
            ]].copy()

            instrmnt_loop['Scenario'] = scenario
            instrmnt_loop['Eco_serv'] = es

            # Merge with depreciation
            dpr_subset = dpr_long[
                (dpr_long['Scenario'] == scenario) &
                (dpr_long['Eco_serv'] == es)
            ][['PERIOD', 'IDENTIFIER', 'Depreciation']]

            instrmnt_loop = instrmnt_loop.merge(
                dpr_subset, on=['PERIOD', 'IDENTIFIER'], how='left'
            )

            # Calculate financial impacts
            result = financial_models.calculate_instrument_impacts(instrmnt_loop)

            results_list.append(result)

        # Combine all results
        final_results = pd.concat(results_list, ignore_index=True)

        return final_results


def main():
    """Main entry point."""
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)
    return results


if __name__ == "__main__":
    results = main()
