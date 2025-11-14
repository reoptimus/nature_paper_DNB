"""
Main pipeline for SHS Nature Analysis
Orchestrates the complete analysis workflow
"""
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import product
import logging

import config
import data_loader
import vulnerability_calc
import financial_models
import visualization

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
        self.instrmnt_df = data_loader.load_instrument_data()
        
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
        output_file = Path('./shs_2024-Q4_results.csv')
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


def main():
    """Main entry point."""
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)
    return results


if __name__ == "__main__":
    results = main()
