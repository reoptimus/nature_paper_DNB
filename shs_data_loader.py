"""
Data loading and preprocessing functions
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List
from . import shs_config as config


def load_instrument_data(file_path: str = config.INSTRUMENT_FILE) -> pd.DataFrame:
    """Load instrument data with proper dtype specification."""
    return pd.read_csv(file_path, dtype={'nace': 'str'})


def load_vulnerability_data(file_path: Path = None) -> pd.DataFrame:
    """Load and reshape vulnerability/dependency score data."""
    if file_path is None:
        file_path = config.VULN_PATH / config.VULN_FILE
    
    df = pd.read_csv(file_path)
    
    # Pivot from wide to long format
    value_cols = [col for col in df.columns if col not in 
                  ['region', 'eco_serv', 'EXIOBASE', 'indout', 'NACE Code', 'Adj_ind']]
    
    df_long = df.melt(
        id_vars=['region', 'eco_serv', 'EXIOBASE', 'indout', 'NACE Code', 'Adj_ind'],
        value_vars=value_cols,
        var_name='Vuln_type',
        value_name='Vuln'
    )
    
    return df_long


def load_alpha_data(file_path: Path = None, 
                    area_map_path: Path = config.AREA_MAP_FILE) -> pd.DataFrame:
    """Load and prepare alpha (shock) data."""
    if file_path is None:
        file_path = config.VULN_PATH / config.ALPHA_FILE
    
    alpha_df = pd.read_excel(file_path)
    area_map = pd.read_csv(area_map_path)
    
    # Reshape and merge
    alpha_df = (
        alpha_df.melt(id_vars=['Area', 'eco_serv'], 
                     var_name='Vuln_type', 
                     value_name='Alpha')
        .merge(area_map, left_on='Area', right_on='area', how='left')
        .drop(columns=['Area', 'area'])
        .rename(columns={
            'eco_serv': 'scenario',
            'region': 'ISSUER_COUNTRY',
            'Alpha': 'alpha'
        })
    )
                       
    return alpha_df


def load_production_data(file_path: Path = config.X_FILE) -> pd.DataFrame:
    """Load EXIOBASE production data (X)."""
    return pd.read_csv(file_path)


def load_nace_mapping(file_path: Path = None, 
                     mapping_type: str = 'detailed') -> pd.DataFrame:
    """
    Load NACE code mapping.
    
    Args:
        file_path: Path to mapping file
        mapping_type: 'simple' for nace_0d_map or 'detailed' for EXIOBASE mapping
    """
    if file_path is None:
        file_path = (config.NACE_MAP_FILE if mapping_type == 'simple' 
                    else config.EXIOBASE_NACE_MAP)
    
    if file_path.suffix == '.xlsx':
        return pd.read_excel(file_path, engine='openpyxl')
    return pd.read_csv(file_path)


def load_shs_holder_data(file_path: str = config.SHS_HOLDER_FILE) -> pd.DataFrame:
    """Load SHS holder-instrument relationship data."""
    return pd.read_csv(file_path)


def extract_scenario_info(df: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
    """Extract unique scenarios, eco services, and aggregation types from data."""
    
    def extract_prefix(strings):
        return [s.split('_DS_total_')[0].split('_Vuln_total_')[0] for s in strings]
    
    scenarios = list(set(extract_prefix(df['Vuln_type'].unique())))
    eco_services = df['eco_serv'].unique().tolist()
    
    return scenarios, eco_services


def prepare_vulnerability_with_alpha(vuln_df: pd.DataFrame, 
                                     alpha_df: pd.DataFrame) -> pd.DataFrame:
    """Merge vulnerability data with alpha shock parameters."""
    
    # Split Vuln_type into base type and option
    vuln_df = vuln_df.copy()
    vuln_df['option'] = vuln_df['Vuln_type'].str.rsplit('_', n=1).str[1]
    vuln_df['Vuln_type'] = vuln_df['Vuln_type'].str.rsplit('_', n=1).str[0]
    
    # Clean alpha data similarly
    alpha_clean = alpha_df.copy()
    alpha_clean['Vuln_type'] = alpha_clean['Vuln_type'].str.rsplit('_', n=1).str[0]
    alpha_clean['option'] = alpha_clean['Vuln_type'].str.rsplit('_', n=1).str[1]
    alpha_clean['Vuln_type'] = alpha_clean['Vuln_type'].str.rsplit('_', n=1).str[0]
    alpha_clean = alpha_clean.rename(columns={
        'scenario': 'eco_serv',
        'ISSUER_COUNTRY': 'region'
    })
    
    # Merge
    merged = vuln_df.merge(
        alpha_clean[['Vuln_type', 'eco_serv', 'region', 'option', 'alpha']],
        on=['Vuln_type', 'eco_serv', 'region', 'option'],
        how='left'
    )
    
    # Calculate production loss
    merged['delta_prod'] = merged['indout'] * merged['Vuln'] * merged['alpha']
    
    return merged


def clean_instrument_maturity(df: pd.DataFrame, 
                              max_maturity: int = config.MAX_MATURITY) -> pd.DataFrame:
    """Clean and impute residual maturity data."""
    df = df.copy()
    
    # Clip maturity to maximum
    df['resid_mat_yr'] = df['resid_mat_yr'].clip(upper=max_maturity)
    
    # Calculate mean maturity for bonds
    bond_mask = (df['INSTR_CLASS'] == 'F_511') & df['resid_mat_yr'].notnull()
    mean_maturity = df.loc[bond_mask, 'resid_mat_yr'].mean()
    
    # Fill missing bond maturities
    fill_mask = (df['INSTR_CLASS'] == 'F_511') & df['resid_mat_yr'].isnull()
    df.loc[fill_mask, 'resid_mat_yr'] = mean_maturity
    
    return df
