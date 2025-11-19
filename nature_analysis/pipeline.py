"""
Main pipeline for SHS Nature Analysis
Orchestrates the complete analysis workflow
"""
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import product
import logging

from . import config
from . import data_loader
from . import vulnerability as vulnerability_calc
from . import financial as financial_models
from . import visualization

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
        
    def prepare_production_loss_analysis(self, 
                                        eco_service: str,
                                        vuln_type: str,
                                        option: str) -> pd.DataFrame:
        """
        Prepare and analyze production losses.
        
        Returns merged dataframe with production loss calculations.
        """
        logger.info(f"Analyzing production loss for {eco_service}")
        
        # Prepare merged data with alpha
        df_merged = data_loader.prepare_vulnerability_with_alpha(
            self.vuln_df, self.alpha_df
        )
        
        return df_merged
    
    def calculate_instrument_depreciations(self) -> pd.DataFrame:
        """
        Calculate depreciations for all instruments across all scenarios.
        
        Returns DataFrame with depreciation columns for each scenario/ES combination.
        """
        logger.info("Calculating instrument depreciations...")
        
        # Use configured eco services or all available
        eco_services = config.ECO_SERVICES if hasattr(config, 'ECO_SERVICES') else self.eco_services
        
        depreciation_df = vulnerability_calc.calculate_all_depreciations(
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
        
        output_file = (config.RESULTS_PATH / 
                      f'merged_SHS_instr_vulnxalpha_scenarios_{config.DEPENDENCY_TYPE}_{config.AGGREG_TYPE}.csv')
        depreciation_df.to_csv(output_file, index=False)
        logger.info(f"Saved depreciation data to {output_file}")

        return depreciation_df

    def calculate_instrument_depreciations_light(self, n_instruments: int = 100) -> pd.DataFrame:
        """
        Lightweight version: Calculate depreciations for limited instruments and scenarios.

        This method is designed for quick testing and demonstration purposes.
        It uses only:
        - First n_instruments instruments (default: 100)
        - First scenario
        - First ecosystem service

        Args:
            n_instruments: Number of instruments to process (default: 100)

        Returns:
            DataFrame with depreciation column for the limited scenario
        """
        logger.info(f"Calculating lightweight depreciations (first {n_instruments} instruments)...")

        # Use configured eco services or all available
        eco_services = config.ECO_SERVICES if hasattr(config, 'ECO_SERVICES') else self.eco_services

        # Limit to first scenario and first ecosystem service
        first_scenario = self.scenarios[0]
        first_eco_service = eco_services[0]

        logger.info(f"Using scenario: {first_scenario}, ecosystem service: {first_eco_service}")

        # Limit instruments to first n_instruments
        instrmnt_subset = self.instrmnt_df.head(n_instruments).copy()

        # Calculate depreciation for the single scenario/ES combination
        depreciation_df = vulnerability_calc.calculate_depreciation(
            self.vuln_df,
            instrmnt_subset,
            self.alpha_df,
            first_eco_service,
            first_scenario,
            config.AGGREG_TYPE,
            self.nace_map,
            config.DEPENDENCY_TYPE
        )

        # Combine with instrument metadata
        final_df = pd.concat([
            instrmnt_subset[['PERIOD', 'IDENTIFIER', 'INSTR_CLASS',
                            'ISSUER_COUNTRY', 'nace_lvl1', 'nace_lvl3']],
            depreciation_df
        ], axis=1)

        logger.info(f"Lightweight depreciation calculation complete: {final_df.shape}")

        return final_df

    def calculate_financial_impacts(self, depreciation_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate financial impacts (PD, LGD, price variations) for all scenarios.
        
        Args:
            depreciation_df: DataFrame with depreciation columns
        
        Returns:
            DataFrame with financial impact calculations
        """
        logger.info("Calculating financial impacts...")
        
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
            logger.info(f"Processing scenario: {scenario}, ES: {es}")
            
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
    
    def calculate_shs_losses(self, financial_impacts: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate SHS holder losses by merging with holder-instrument data.
        
        Args:
            financial_impacts: DataFrame with price variations
        
        Returns:
            DataFrame with aggregated losses by holder
        """
        logger.info("Calculating SHS holder losses...")
        
        # Load holder-instrument data
        shs_holder_df = data_loader.load_shs_holder_data()
        
        # Select relevant columns from financial impacts
        merge_cols = ['PERIOD', 'IDENTIFIER', 'INSTR_CLASS', 'ISSUER_COUNTRY',
                     'ISSUER_SECTOR', 'Scenario', 'Eco_serv']
        impact_subset = financial_impacts[merge_cols + 
                                         ['p_var', 'Security_type', 
                                          'resid_mat_yr', 'nace_lvl1']]
        
        # Merge with holder data
        shs_results = impact_subset.merge(
            shs_holder_df,
            on=['PERIOD', 'IDENTIFIER'],
            how='left'
        )
        
        # Calculate value loss
        shs_results['VALUE_LOSS'] = shs_results['p_var'] * shs_results['OBS_VALUE']
        
        # Select and aggregate
        result_cols = ['HOLDER_SECTOR', 'HOLDER_AREA', 'Security_type', 
                      'nace_lvl1', 'ISSUER_COUNTRY', 'VALUE_LOSS', 
                      'OBS_VALUE', 'Eco_serv', 'Scenario']
        
        shs_results = shs_results[result_cols].groupby(
            ['HOLDER_SECTOR', 'HOLDER_AREA', 'Security_type', 
             'nace_lvl1', 'ISSUER_COUNTRY', 'Eco_serv', 'Scenario'],
            as_index=False
        ).sum()
        
        # Save results
        output_file = config.RESULTS_PATH / 'shs_2024-Q4_results.csv'
        shs_results.to_csv(output_file, index=False)
        logger.info(f"Saved SHS results to {output_file}")
        
        return shs_results
    
    def run_full_pipeline(self, create_plots: bool = True):
        """
        Run the complete analysis pipeline.
        
        Args:
            create_plots: Whether to generate visualization plots
        """
        logger.info("=" * 60)
        logger.info("Starting SHS Nature Analysis Pipeline")
        logger.info("=" * 60)
        
        # Step 1: Load data
        self.load_all_data()
        
        # Step 2: Calculate depreciations
        depreciation_df = self.calculate_instrument_depreciations()
        
        # Step 3: Calculate financial impacts
        financial_impacts = self.calculate_financial_impacts(depreciation_df)
        
        # Step 4: Calculate SHS losses
        shs_results = self.calculate_shs_losses(financial_impacts)
        
        # Step 5: Optional visualizations
        if create_plots:
            logger.info("Creating visualizations...")
            self.create_visualizations(shs_results)
        
        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)

        return shs_results

    def run_quick_test(self, n_instruments: int = 100) -> pd.DataFrame:
        """
        Run a quick test of the pipeline with limited data.

        This is a lightweight version designed for fast testing and demonstration.
        Uses only:
        - First n_instruments instruments (default: 100)
        - First scenario
        - First ecosystem service

        Args:
            n_instruments: Number of instruments to process (default: 100)

        Returns:
            DataFrame with depreciation results for the limited scenario

        Example:
            >>> pipeline = AnalysisPipeline()
            >>> results = pipeline.run_quick_test(n_instruments=50)
            >>> print(f"Processed {len(results)} instruments")
        """
        logger.info("=" * 60)
        logger.info(f"Starting Quick Test Pipeline (n={n_instruments} instruments)")
        logger.info("=" * 60)

        # Step 1: Load data
        self.load_all_data()

        # Step 2: Calculate depreciations (lightweight)
        depreciation_df = self.calculate_instrument_depreciations_light(n_instruments)

        logger.info("=" * 60)
        logger.info("Quick test completed successfully!")
        logger.info(f"Processed {len(depreciation_df)} instruments")
        logger.info("=" * 60)

        return depreciation_df

    def create_visualizations(self, shs_results: pd.DataFrame):
        """Create standard visualization outputs."""
        
        # Example: Create heatmap for one scenario
        eco_service = 'Water flow regulation'
        scenario = '1_World_shock_10perc_02_GOVonNFC'
        
        try:
            fig = visualization.plot_loss_heatmap_by_dimension(
                shs_results,
                eco_service=eco_service,
                scenario=scenario,
                dimension_x='nace_lvl1',
                dimension_y='HOLDER_SECTOR',
                value_type='percentage'
            )
            
            output_path = config.ANALYSIS_PATH / f'heatmap_{eco_service}_{scenario}.png'
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved heatmap to {output_path}")
            
        except Exception as e:
            logger.warning(f"Could not create visualization: {e}")


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

    def calculate_instrument_depreciations(self) -> pd.DataFrame:
        """
        Calculate depreciations for all AnaCredit instruments across all scenarios.

        Returns DataFrame with depreciation columns for each scenario/ES combination.
        """
        logger.info("Calculating AnaCredit instrument depreciations...")

        # Use configured eco services or all available
        eco_services = config.ECO_SERVICES if hasattr(config, 'ECO_SERVICES') else self.eco_services

        depreciation_df = vulnerability_calc.calculate_all_anacredit_depreciations(
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

        output_file = (config.RESULTS_PATH /
                      f'merged_AnaCredit_instr_vulnxalpha_scenarios_{config.DEPENDENCY_TYPE}_{config.AGGREG_TYPE}.csv')
        depreciation_df.to_csv(output_file, index=False)
        logger.info(f"Saved AnaCredit depreciation data to {output_file}")

        return depreciation_df

    def calculate_instrument_depreciations_light(self, n_instruments: int = 100) -> pd.DataFrame:
        """
        Lightweight version: Calculate depreciations for limited AnaCredit instruments.

        Args:
            n_instruments: Number of instruments to process (default: 100)

        Returns:
            DataFrame with depreciation column for the limited scenario
        """
        logger.info(f"Calculating lightweight AnaCredit depreciations (first {n_instruments} instruments)...")

        # Use configured eco services or all available
        eco_services = config.ECO_SERVICES if hasattr(config, 'ECO_SERVICES') else self.eco_services

        # Limit to first scenario and first ecosystem service
        first_scenario = self.scenarios[0]
        first_eco_service = eco_services[0]

        logger.info(f"Using scenario: {first_scenario}, ecosystem service: {first_eco_service}")

        # Limit instruments to first n_instruments
        instrmnt_subset = self.instrmnt_df.head(n_instruments).copy()

        # Calculate depreciation for the single scenario/ES combination
        depreciation_df = vulnerability_calc.calculate_anacredit_depreciation(
            self.vuln_df,
            instrmnt_subset,
            self.alpha_df,
            first_eco_service,
            first_scenario,
            config.AGGREG_TYPE,
            self.nace_map,
            config.DEPENDENCY_TYPE
        )

        # Combine with instrument metadata
        final_df = pd.concat([
            instrmnt_subset[['PERIOD', 'IDENTIFIER', 'INSTR_CLASS',
                            'ISSUER_COUNTRY', 'nace_lvl2','nace_lvl4']],
            depreciation_df
        ], axis=1)

        logger.info(f"Lightweight AnaCredit depreciation calculation complete: {final_df.shape}")

        return final_df

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

    def run_full_pipeline(self, create_plots: bool = False):
        """
        Run the complete AnaCredit analysis pipeline.

        Args:
            create_plots: Whether to generate visualization plots
        """
        logger.info("=" * 60)
        logger.info("Starting AnaCredit Nature Analysis Pipeline")
        logger.info("=" * 60)

        # Step 1: Load data
        self.load_all_data()

        # Step 2: Calculate depreciations
        depreciation_df = self.calculate_instrument_depreciations()

        # Step 3: Calculate financial impacts
        financial_impacts = self.calculate_financial_impacts(depreciation_df)

        # Step 4: Save results
        output_file = config.RESULTS_PATH / 'anacredit_financial_impacts.csv'
        financial_impacts.to_csv(output_file, index=False)
        logger.info(f"Saved AnaCredit financial impacts to {output_file}")

        logger.info("=" * 60)
        logger.info("AnaCredit Pipeline completed successfully!")
        logger.info("=" * 60)

        return financial_impacts

    def run_quick_test(self, n_instruments: int = 100) -> pd.DataFrame:
        """
        Run a quick test of the AnaCredit pipeline with limited data.

        Args:
            n_instruments: Number of instruments to process (default: 100)

        Returns:
            DataFrame with depreciation results for the limited scenario
        """
        logger.info("=" * 60)
        logger.info(f"Starting AnaCredit Quick Test Pipeline (n={n_instruments} instruments)")
        logger.info("=" * 60)

        # Step 1: Load data
        self.load_all_data()

        # Step 2: Calculate depreciations (lightweight)
        depreciation_df = self.calculate_instrument_depreciations_light(n_instruments)

        logger.info("=" * 60)
        logger.info("AnaCredit quick test completed successfully!")
        logger.info(f"Processed {len(depreciation_df)} instruments")
        logger.info("=" * 60)

        return depreciation_df


def main():
    """Main entry point."""
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)
    return results


if __name__ == "__main__":
    results = main()
