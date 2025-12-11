"""
Data loading and preprocessing functions
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List
from . import config


def load_SHS_data(file_path: str = config.SHS_INSTRUMENT_FILE) -> pd.DataFrame:
    """Load SHS instrument data with proper dtype specification."""
    SHS_instrmnt = pd.read_csv(file_path, dtype={'nace': 'str'})
    return SHS_instrmnt

def load_Anacredit_data(file_path: str = config.ANACREDIT_INSTRUMENT_FILE) -> pd.DataFrame:
    """Load SHS instrument data with proper dtype specification."""
    anacredit_instrmnt = pd.read_csv(file_path, dtype={'nace': 'str'})
    # anacredit_instrmnt = pd.read_csv(config.ANACREDIT_INSTRUMENT_FILE)
    # add INSTR_CLASS , vol and debt_ratio to be coherent with SHS data frame
    # INSTR_CLASS
    anacredit_instrmnt['INSTR_CLASS'] = 'Loan_Anacredit'
    # vol
    volatilities_lvl2 = pd.read_excel( config.VOL_FILE )
    volatilities_lvl2['vol'] = volatilities_lvl2['vol']/100
    anacredit_instrmnt = anacredit_instrmnt.merge(volatilities_lvl2, left_on= 'nace_level_2', right_on = 'nace_lvl2', how = 'left' , validate='m:1' )
    anacredit_instrmnt = anacredit_instrmnt.drop(columns=['nace_lvl2'])
    # debt_ratio
    debt_ratio_lvl2 = pd.read_excel( config.DEBT_RATIO_FILE )
    anacredit_instrmnt = anacredit_instrmnt.merge(debt_ratio_lvl2, left_on= 'nace_level_2', right_on = 'nace_lvl2', how = 'left' , validate='m:1')
    anacredit_instrmnt = anacredit_instrmnt.drop(columns=['nace_lvl2'])
    # to be delteted just for coding test purpose
    # anacredit_instrmnt = anacredit_instrmnt[1:2000]
    return anacredit_instrmnt

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

    # modification of field Vuln_type with creation of one column for option (SR or max)
    # Extract option (the part before _alpha)
    alpha_df['option'] = alpha_df['Vuln_type'].str.extract(r'_([^_]+)_alpha$')
    # Remove the "_option_alpha" part from the original string
    alpha_df['Vuln_type'] = alpha_df['Vuln_type'].str.replace(r'_[^_]+_alpha$', '', regex=True)

    return alpha_df

def load_production_data(file_path: Path = config.EXIOBASE_X_VECTOR) -> pd.DataFrame:
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


def prepare_vulnerability_with_alpha(vuln_df_: pd.DataFrame, 
                                     alpha_df_: pd.DataFrame) -> pd.DataFrame:
    """Merge vulnerability data with alpha shock parameters."""
    
    # Split Vuln_type into base type and option
    vuln_df_clean = vuln_df_.copy()
    vuln_df_clean['option'] = vuln_df_clean['Vuln_type'].str.rsplit('_', n=1).str[1]
    vuln_df_clean['Vuln_type'] = vuln_df_clean['Vuln_type'].str.rsplit('_', n=1).str[0]
    
    # Clean alpha data similarly
    alpha_clean = alpha_df_.copy()
    alpha_clean = alpha_clean.rename(columns={
        'scenario': 'eco_serv',
        'ISSUER_COUNTRY': 'region'
    })
    
    # Merge
    merged = vuln_df_clean.merge(
        alpha_clean[['Vuln_type', 'eco_serv', 'region', 'option', 'alpha']],
        on=['Vuln_type', 'eco_serv', 'region', 'option'],
        how='left'
    )
    
    # Calculate production loss
    merged['delta_indout'] = merged['indout'] * merged['Vuln'] * merged['alpha']
    
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

def load_COREP_data(file_path: str = config.COREP_FILE) -> pd.DataFrame:
    """Load COREP data with proper dtype specification."""
    COREP_data = pd.read_csv(file_path)
    return COREP_data

def load_S2_ARS_data_BS(file_path: str = config.S2_ARS_FILE) -> pd.DataFrame:
    # Read csv file with ARS extract
    print("Reading ARS extract...")
    ARS_extract = download_csv_to_pandas( remote_filepath = file_path ) # ARS_extract = download_csv_to_pandas(  config.S2_ARS_FILE  )

    # Check unique periods
    print("Unique periods:", ARS_extract['periode'].unique())

    # List of fields to delete
    list_deleted_fields = [
        "rapportageset", "formulier_id", "inzendmoment", "laad_dts", "eind_dts",
        "categorie", "verkorte_naam", "toezichtklasse", "activiteitstatus",
        "hoofdcategorie", "subcategorie", "ziektekosten", "rechtsopvolger", "A"
    ]

    # Remove specified columns
    ARS_extract = ARS_extract.drop(columns=list_deleted_fields, errors='ignore')

    # Remove columns ending with 'C0020'
    ARS_extract = ARS_extract.loc[:, ~ARS_extract.columns.str.endswith('C0020')]

    # Remove columns starting with 'R1000'
    ARS_extract = ARS_extract.loc[:, ~ARS_extract.columns.str.startswith('R1000')]

    # Filter for specific period
    ARS_extract = ARS_extract[ARS_extract['periode'] == '31/12/2024']

    # Get unique concern names
    print("Unique concern names:", ARS_extract['concern_naam'].unique())

    # For each insurer, keep the report with highest 'volgnummer'
    print("Filtering for highest volgnummer per insurer...")
    list_report = (
        ARS_extract[['relatienummer', 'relatienaam', 'rapportageID', 'volgnummer']]
        .drop_duplicates()
        .sort_values('volgnummer', ascending=False)
        .groupby('relatienummer', as_index=False)
        .first()
        .sort_values('relatienummer')
    )

    # Filter for last volgnummer per reporting entity
    ARS_extract = ARS_extract[ARS_extract['rapportageID'].isin(list_report['rapportageID'])]

    # Convert "NA" string to empty string
    ARS_extract = ARS_extract.replace("NA", "")

    # Convert columns starting with "R0" to numeric
    print("Converting R0 columns to numeric...")
    r0_cols = [col for col in ARS_extract.columns if col.startswith('R0')]
    for col in r0_cols:
        ARS_extract[col] = pd.to_numeric(ARS_extract[col], errors='coerce')

    # Pivot from wide to long format
    print("Pivoting data to long format...")
    id_cols = [col for col in ARS_extract.columns if not col.startswith('R0')]
    a = pd.melt(
        ARS_extract,
        id_vars=id_cols,
        value_vars=r0_cols,
        var_name='BS_items_ID',
        value_name='BS_item_value'
    )

    # Filter for top insurers from the correspondance table between internal_number (ARS) and LEI/RIAD to join SHS
    print("Filtering for top insurers from SHS...")
    list_insurers_LEI = download_excel_to_pandas( remote_filepath = config.Corresp_RelatieNum_LEI ) 
    list_insurers_LEI = list_insurers_LEI[list_insurers_LEI['relatienummer1'] != '#N/A']
    QRS_short = (
        a.merge(
            list_insurers_LEI[['relatienummer1', 'LEI', 'RIAD']],
            left_on='relatienummer',
            right_on='relatienummer1',
            how='inner'
        )
        .drop(columns='relatienummer1')
    )

    # Pivot back to wide format (insurers as columns)
    print("Pivoting data to wide format...")
    QRS_tab = QRS_short.pivot_table(
            index='BS_items_ID',
            columns='LEI',
            values='BS_item_value',
            aggfunc='first'  # Use 'first' to handle any duplicates
        ).reset_index().sort_values('BS_items_ID')

    # Extract first 5 characters of BS_items_ID
    QRS_tab['BS_items_ID'] = QRS_tab['BS_items_ID'].str[:5]

    # Add label names to balance sheet items
    print("Adding labels to balance sheet items...")
    labels_ARS =  download_excel_to_pandas( remote_filepath = config.S2_01_01_template )
    labels_ARS.columns = ['BS_categories_names','BS_items_ID']

    # Merge BS_items_ID to labels
    QRS_tab = QRS_tab.merge(labels_ARS , on = 'BS_items_ID' , how = 'left')


    # Reorder columns to put items_labels and BS_items_ID first
    cols = ['BS_categories_names', 'BS_items_ID'] + [
        col for col in QRS_tab.columns
        if col not in ['BS_categories_names', 'BS_items_ID']
    ]
    QRS_tab = QRS_tab[cols]
    return QRS_tab

def load_S2_ARS_data_SCR(file_path: str = config.S2_ARS_FILE_SCR ) -> pd.DataFrame:
    # Read csv file with ARS extract
    print("Reading ARS extract...")
    ARS_extract = download_csv_to_pandas( remote_filepath = file_path ) #  ARS_extract =download_csv_to_pandas(  config.S2_ARS_FILE_SCR  )

    # Filter for specific period
    ARS_extract = ARS_extract[ARS_extract['periode'] == '31-12-2024']
    # Check unique periods
    print("Unique periods:", ARS_extract['periode'].unique())

    # For each insurer, keep the report with highest 'volgnummer'
    print("Filtering for highest volgnummer per insurer...")
    list_report = (
        ARS_extract[['relatienummer', 'relatienaam', 'rapportageID', 'volgnummer']]
        .drop_duplicates()
        .sort_values('volgnummer', ascending=False)
        .groupby('relatienummer', as_index=False)
        .first()
        .sort_values('relatienummer')
    )

    # Filter for last volgnummer per reporting entity
    ARS_extract = ARS_extract[ARS_extract['rapportageID'].isin(list_report['rapportageID'])]

    # SCR net info is C0030 code
    # Define the data for rows code and names
    scr_table = pd.DataFrame({
        "SCR Category": [
            "Market risk",
            "Counterparty default risk",
            "Life underwriting risk",
            "Health underwriting risk",
            "Non-life underwriting risk",
            "Diversification",
            "Intangible asset risk",
            "Basic Solvency Capital Requirement"
        ],
        "Code": [
            "R0010",
            "R0020",
            "R0030",
            "R0040",
            "R0050",
            "R0060",
            "R0070",
            "R0100"
        ]
    })
 
    # filter ARS_extract
    keep_list = ['relatienummer', 'R0010C0030', 'R0100C0030']
    ARS_extract = ARS_extract[keep_list]

    # Filter for top insurers from the correspondance table between internal_number (ARS) and LEI/RIAD to join SHS
    print("Filtering for top insurers from SHS...")
    list_insurers_LEI = download_excel_to_pandas( remote_filepath = config.Corresp_RelatieNum_LEI ) 
    list_insurers_LEI = list_insurers_LEI[list_insurers_LEI['relatienummer1'] != '#N/A']
    ARS_short = (
        ARS_extract.merge(
            list_insurers_LEI[['relatienummer1', 'LEI', 'RIAD']],
            left_on='relatienummer',
            right_on='relatienummer1',
            how='inner'
        )
        .drop(columns='relatienummer1')
    )

    # rename columns names
    ARS_short = ARS_short.rename(columns={ 'R0010C0030' : 'Market risk SCR' , 'R0100C0030' : 'basic SCR' })
    return ARS_short

def aggregate_shs_losses(input_path, output_path):
    """
    Aggregates SHS losses for ease of analysis and data presentation.

    Steps:
    1. Read the Excel file from input_path.
    2. Withdraw (drop) columns ['INSTR_CLASS', 'nace_lvl2', 'loss_perc'].
    3. Identify all remaining columns except the ones to aggregate.
    4. Aggregate VALUE_LOSS and OBS_VALUE by all other columns.
    5. Save the aggregated results to output_path.
    """
    # 1. Read the file back
    df = pd.read_excel(input_path)

    # 2. Withdraw (drop) the listed columns
    df_subset = df.drop(columns=['INSTR_CLASS', 'nace_lvl2', 'loss_perc'])

    # 3.1 Identify all columns except the ones to aggregate
    group_cols = [col for col in df_subset.columns if col not in ['VALUE_LOSS', 'OBS_VALUE']]

    # 3.2 Aggregate VALUE_LOSS and OBS_VALUE by all other columns
    agg_df = df.groupby(group_cols, as_index=False).agg({
        'VALUE_LOSS': 'sum',
        'OBS_VALUE': 'sum'
    })

    # 4. Save the aggregated results
    agg_df.to_excel(output_path, index=False)
    # Example usage:
    # aggregate_shs_losses(
    #     config.RESULTS_PATH / "SHS_Losses_all_scenario_ecosystem.xlsx",
    #     config.RESULTS_PATH / "SHS_Losses_aggregated_lvl1.xlsx")
    return agg_df


"""
##########################################
#||                                    #||
#|| Azure containers class & functions #||
#||                                    #||
##########################################
"""

import os
from enum import Enum
from io import BytesIO
from pprint import pprint

import pandas as pd
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceModifiedError

# ----------------------------
# Authentication / Credentials
# ----------------------------

class LoginMethod(Enum):
    AZCLI = AzureCliCredential()
    SAS = os.environ.get("DATALAKE_STORAGE_SAS", None)
    ACCOUNT_KEY = os.environ.get("DATALAKE_STORAGE_ACCOUNT_KEY", None)
    account_name = config.account_name
    container_name = config.container_name

    def get_service_client(self, account_name):
        self.account_url = f"https://{account_name}.dfs.core.windows.net"
        return DataLakeServiceClient(self.account_url, credential=self.value)

    def get_file_system_client(self, account_name, container_name):
        return self.get_service_client(account_name).get_file_system_client(
            container_name
        )

    def get_directory_client(self, account_name, container_name, directory_path="/"):
        return self.get_service_client(account_name).get_directory_client(
            container_name, directory=directory_path
        )

    def get_file_client(self, account_name, container_name, file_path):
        return self.get_service_client(account_name).get_file_client(
            container_name, file_path
        )

# ----------------------------
# File operations
# ----------------------------

def upload_file(
    account_name: str,
    container_name: str,
    remote_filepath: str,
    local_filepath: str,
    method: LoginMethod,  # e.g., LoginMethod.AZCLI
    overwrite: bool = False,
):
    """
    Upload a file to the DSAT Multistorage solution
    Parameters:
    account_name (str): Name of the Multistorage account
    container_name (str): Name of the container inside the multistorage that we should upload to
    remote_filepath (str): Destination filepath after the upload completes
    local_filepath (str): Path to the file on the local filesystem that should be uploaded
    method (LoginMethod): How to Authenticate to the Multistorage solution
    overwrite (bool): Should we overwrite the file in the multistorage container if it already exists?
    """
    client = method.get_file_client(account_name, container_name, remote_filepath)

    if not client.exists():
        print("Destination File doesnt exist yet, creating...")
        client.create_file()
        overwrite=True

    try:
        with open(local_filepath, "rb") as source_data:
            client.upload_data(source_data, overwrite=overwrite)
    except ResourceModifiedError:
        raise FileExistsError(f"File {method.account_url+'/'+container_name+'/'+remote_filepath} already exists!\nSet the overwrite flag to True if you wish to overwrite the file.")


def download_file(
    account_name: str,
    container_name: str,
    remote_filepath: str,
    local_filepath: str,
    method=LoginMethod.AZCLI,  # e.g., LoginMethod.AZCLI
    overwrite: bool = False,
):
    """
    Download a file from the DSAT Multistorage solution
    Parameters:
    account_name (str): Name of the Multistorage account
    container_name (str): Name of the container inside the multistorage that we should upload to
    remote_filepath (str): Path to the file in the Multistorage container that should be downloaded
    local_filepath (str): Path of the file on the local filesystem after the download completes.
    method (LoginMethod): How to Authenticate to the Multistorage solution
    overwrite (bool): Should we overwrite the file on the local filesystem if it already exists?
    """
    client = method.get_file_client(account_name, container_name, remote_filepath)
    download_stub = client.download_file()

    write_flags = "wb" if overwrite else "xb"

    try:
        with open(local_filepath, write_flags) as f:
            f.write(download_stub.readall())
    except FileExistsError:
        raise FileExistsError(f"Local File {local_filepath} already exists!\nSet the overwrite flag to True if you wish to overwrite the file.")

# ----------------------------
# Pandas helpers
# ----------------------------

def _download_to_bytesio(
    remote_filepath: str,
    account_name: str = config.account_name,
    container_name: str = config.container_name,
    method: LoginMethod = LoginMethod.AZCLI ,  # e.g., LoginMethod.AZCLI
) -> BytesIO:
    """
    Download remote file into an in-memory BytesIO stream (rewound to position 0).
    """
    file_client = method.get_file_client(account_name, container_name, remote_filepath)
    downloader = file_client.download_file()
    buf = BytesIO()
    downloader.readinto(buf)
    buf.seek(0)
    return buf

def download_csv_to_pandas( 
    remote_filepath: str,
    account_name: str,
    container_name: str,
    method=LoginMethod.AZCLI,
):
    """
    Fetch a CSV file from the DSAT Multistorage solution and make it available as a Pandas Dataframe
    Parameters:
    account_name (str): Name of the Multistorage account
    container_name (str): Name of the container inside the multistorage that we should upload to
    remote_filepath (str): Path to the file in the Multistorage container that should be downloaded
    method (LoginMethod): How to Authenticate to the Multistorage solution

    Returns:
    pd.DataFrame: Pandas Dataframe holding the CSV data downloaded from the multistorage container.
    """
    input_blob = _download_to_bytesio( remote_filepath, account_name, container_name, method)
    input_blob.seek(0)
    return pd.read_csv(input_blob, sep=",")

def download_excel_to_pandas(
    remote_filepath: str,
    account_name: str = config.account_name,
    container_name: str = config.container_name,
    method: LoginMethod = LoginMethod.AZCLI ,  # e.g., LoginMethod.AZCLI
    sheet_name=0) -> pd.DataFrame:
    """
    Download an Excel file from ADLS Gen2 and parse it as a pandas DataFrame.

    Uses 'openpyxl' for .xlsx and 'xlrd' for legacy .xls automatically (based on extension).
    """
    input_blob = _download_to_bytesio( remote_filepath, account_name, container_name, method)
    input_blob.seek(0)

    # download_stub.readinto(input_blob)
    ext = Path(remote_filepath).suffix.lower()
    if ext == ".xls":
        # Requires xlrd installed (modern xlrd supports only .xls)
        pandas_df = pd.read_excel(input_blob, sheet_name=sheet_name, engine="xlrd")
    else:
        # Default to .xlsx engine
        pandas_df = pd.read_excel(input_blob, sheet_name=sheet_name, engine="openpyxl")
    return pandas_df

# ----------------------------
# Examples
# ----------------------------

if __name__ == "__main__":

    # Example 1: Download an Excel file into pandas
    remote_xlsx = "secure/Sebastien/Nature 3.0/Nature_analysis/ARS_solva2/Corresp_tabl_relatienummer_LEI.xlsx"
    df_xlsx = download_excel_to_pandas(
        remote_filepath=remote_xlsx,
        account_name=config.account_name,
        container_name=config.container_name,
        method= LoginMethod.AZCLI,  # or LoginMethod.DEFAULT / SAS / ACCOUNT_KEY
        sheet_name=0  )
    print(df_xlsx.head())

