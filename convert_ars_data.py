"""
Convert ARS (Annual Reporting Supervision) S02.01 data processing from R to Python.
This script processes insurance balance sheet data and filters for top insurers.
"""

import pandas as pd
import numpy as np
import os

# Read Excel file with ARS extract
print("Reading ARS extract...")
ARS_extract = pd.read_excel(
    '../Raw_extract_todelete/data_S2QRS_S02_01_20221231.xlsx',
    sheet_name=0
)

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
ARS_extract = ARS_extract[ARS_extract['periode'] == '2022-12-31']

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

# Alternative approach that matches R logic more closely:
# list_report = (
#     ARS_extract[['relatienummer', 'relatienaam', 'rapportageID', 'volgnummer']]
#     .drop_duplicates()
#     .loc[lambda df: df.groupby('relatienummer')['volgnummer'].transform('max') == df['volgnummer']]
#     .sort_values('relatienummer')
# )

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

# Filter for top insurers from MSR
print("Filtering for top insurers from MSR...")
list_insurers_MSR = pd.read_csv('../Balance sheet/List_insurers_MSR_ARS.csv')
list_insurers_MSR = list_insurers_MSR[list_insurers_MSR['relatienummer1'] != '#N/A']
list_insurers_MSR = list_insurers_MSR.drop(columns=['relatienummer2'], errors='ignore')

QRS_short = a[a['relatienummer'].isin(list_insurers_MSR['relatienummer1'])]

# Verify list of insurers in MSR
print("Insurers in MSR:", QRS_short['relatienaam'].unique())

# Pivot back to wide format (insurers as columns)
print("Pivoting data to wide format...")
QRS_tab = (
    QRS_short.pivot_table(
        index='BS_items_ID',
        columns='relatienaam',
        values='BS_item_value',
        aggfunc='first'  # Use 'first' to handle any duplicates
    )
    .reset_index()
    .sort_values('BS_items_ID')
)

# Extract first 5 characters of BS_items_ID
QRS_tab['BS_items_ID'] = QRS_tab['BS_items_ID'].str[:5]

# Add label names to balance sheet items
print("Adding labels to balance sheet items...")
labels_ARS = pd.read_excel('../templates/s02_01_01.xlsx', sheet_name=0)

# Map BS_items_ID to labels using the first column ('NA.') and 'Assets' column
# The R code: labels_ARS$Assets[match(QRS_tab$BS_items_ID, labels_ARS$NA.)]
QRS_tab['items_labels'] = QRS_tab['BS_items_ID'].map(
    labels_ARS.set_index('NA.')['Assets'].to_dict()
)

# Reorder columns to put items_labels and BS_items_ID first
cols = ['items_labels', 'BS_items_ID'] + [
    col for col in QRS_tab.columns
    if col not in ['items_labels', 'BS_items_ID']
]
QRS_tab = QRS_tab[cols]

# Write to CSV
print("Writing output to CSV...")
os.makedirs('./Extra_data', exist_ok=True)
QRS_tab.to_csv('./Extra_data/QRS_tab_20221231.csv', index=False)

print("Done! Output saved to ./Extra_data/QRS_tab_20221231.csv")
