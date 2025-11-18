# Data Directory

This directory should contain the data files required for the nature-based financial risk analysis.

## Required Data Files

The following data files should be placed in your local environment (paths configured in `nature_analysis/config.py`):

### Instrument Data
- **SHS Instrument Data**: Securities Holdings Statistics instrument data
  - Configured path: `INSTRUMENT_FILE` in config.py
  - Expected location: `G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv`

- **AnaCredit Instrument Data**: AnaCredit instrument data (same structure as SHS)
  - Configured path: `ANACREDIT_INSTRUMENT_FILE` in config.py
  - Expected location: `G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/anacredit_instrmnt_nature_prepped.csv`

### Vulnerability and Shock Data
- **Vulnerability Data**: Ecosystem vulnerability scores
  - File: `Vuln_final_03_11_2025.csv`
  - Location: Configured via `VULN_PATH` in config.py

- **Alpha Shock Data**: Shock parameters
  - File: `Alpha_final_03_11_2025.xlsx`
  - Location: Configured via `VULN_PATH` in config.py

### Mapping Data
- **NACE Mappings**: Sector classification mappings
  - `nace_0d_map.xlsx`
  - `EXIOBASE_to_NACElvl2_tab.xlsx`
  - Location: Configured via `DATA_PATH` in config.py

- **Area Mappings**: Regional/country mappings
  - `regions_ISO2_continent_area.csv`
  - Location: Configured via `DATA_PATH` in config.py

### Holder Data (SHS only)
- **SHS Holder Data**: Securities holder-instrument relationships
  - File: `F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv`
  - Location: `H:/Documents/SHS/prepped/`

## Data Structure Requirements

Both SHS and AnaCredit instrument data must have the same structure:
- `PERIOD`: Time period
- `IDENTIFIER`: Unique instrument identifier (e.g., ISIN)
- `INSTR_CLASS`: Instrument class (e.g., F_511 for bonds)
- `ISSUER_COUNTRY`: ISO country code
- `ISSUER_SECTOR`: Sector classification
- `pd`: Probability of default
- `vol`: Volatility
- `debt_ratio`: Debt to assets ratio
- `nace`: NACE sector code
- `nace_lvl*`: NACE codes at different hierarchical levels
- `resid_mat_yr`: Residual maturity in years

## Git Ignore Policy

Data files are intentionally **not tracked by Git** for these reasons:
1. Large file sizes unsuitable for version control
2. Potential sensitive financial data
3. Data should be managed separately from code

Only these data files are allowed in Git (if needed for testing):
- Files ending with `_prepped.csv`
- Files starting with `Vuln_`, `Alpha_`, or `EXIOBASE_`

## Notes

- Update paths in `nature_analysis/config.py` to match your local environment
- Ensure data files have appropriate access permissions
- Keep data files backed up separately from the Git repository
