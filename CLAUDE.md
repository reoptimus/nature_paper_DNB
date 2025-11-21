# Guide for AI Assistants

> **Context-specific guidance for Claude and other AI assistants working on the Nature-Based Financial Risk Analysis package**

---

## Project Overview

This is a **production-ready financial risk analysis package** for quantifying how ecosystem service disruptions impact financial portfolios through credit risk modeling. The code implements the **Merton structural credit risk framework** with real-world data from central banks.

### Critical Context

- **Domain**: Financial risk modeling + Ecosystem science
- **Stakeholder**: Central banks (DNB - Dutch Central Bank)
- **Data**: Two sources - Securities Holdings Statistics (SHS) and AnaCredit (bank lending)
- **Output**: Portfolio value losses from nature-based risks
- **Precision Required**: High - these are real financial calculations

---

## Priority Guidelines When Working on This Codebase

### 1. **Always Start with Configuration**

Read `nature_analysis/config.py` first to understand:
- Financial parameters (PD_CALIB, LGD_CALIB, RISK_FREE_RATE)
- File paths and data sources (SHS vs AnaCredit)
- Analysis settings (AGGREG_TYPE, DEPENDENCY_TYPE)
- Ecosystem services being analyzed

### 2. **Use the Appropriate Pipeline Class**

The package supports **two data sources** with dedicated pipeline classes:

```python
# ✓ CORRECT: Use SHS pipeline for securities holdings data
from nature_analysis import SHSAnalysisPipeline
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline()

# ✓ CORRECT: Use AnaCredit pipeline for bank lending data
from nature_analysis import AnaCreditAnalysisPipeline
pipeline = AnaCreditAnalysisPipeline()
results = pipeline.run_full_pipeline()

# ✗ AVOID: Direct function calls (unless debugging)
from nature_analysis import vulnerability
dep_df = vulnerability.calculate_depreciation(...)
```

**Key Differences:**
- **SHS Pipeline**: Securities holdings → Portfolio losses by holder sector/geography
- **AnaCredit Pipeline**: Bank lending → Financial impacts by instrument (no holder aggregation)

### 3. **Validate All Changes**

**ALWAYS** run tests after making changes:

```bash
# Quick test first (fast validation)
python -c "import nature_analysis; nature_analysis.run_quick_test(n_instruments=10)"

# Full test suite (comprehensive validation)
python tests/test_suite.py
```

The test suite compares outputs against validated reference data. If tests fail, investigate why before proceeding.

**Pro tip:** Use `run_quick_test()` during development for fast iteration, then run the full test suite before finalizing changes.

### 4. **Preserve Financial Accuracy**

The financial models are mathematically precise implementations of academic literature:

- **Merton model equations**: Do not modify unless you fully understand the theory
- **PD/DD conversions**: These use inverse cumulative normal distributions
- **LGD formula**: Incorporates correlation structure
- **Bond pricing**: Credit-risky bond valuation formula

**If you're unsure about a financial formula, ask rather than guess.**

### 5. **Consider Performance**

This package processes large datasets:
- ~50,000 instruments (SHS) or variable (AnaCredit)
- Multiple ecosystem services
- Multiple scenarios
- Parallel processing is used extensively

When modifying code, consider:
- Memory usage (DataFrames can be large)
- Computation time (use parallel processing where appropriate)
- Data types (use categorical for repeated strings)

---

## Vulnerability Data Generation (Optional Workflow)

### Overview

The package uses **vulnerability scores** and **alpha shock parameters** that quantify how ecosystem service disruptions affect economic sectors by country. These files (`Vuln_final.csv` and `Alpha_final.xlsx`) are **pre-generated and stored** in the data directory.

**You typically DON'T need to regenerate these files** unless:
- Updating ENCORE ecosystem service dependency ratings
- New EXIOBASE multi-regional input-output data is available
- Modifying scenario configurations or shock parameters
- Conducting custom sensitivity analyses

### Two Workflows

| Workflow | When to Use | Time Required | Files Used |
|----------|-------------|---------------|------------|
| **Standard** (Recommended) | Regular analysis | Minutes | Pre-generated Vuln/Alpha files |
| **Regeneration** (Optional) | Updating vulnerability data | 10-30 minutes | ENCORE, EXIOBASE, ND-GAIN raw data |

### Vulnerability Generation Module

The `vulnerability_generator.py` module creates vulnerability files from:

**Input Data Sources:**
1. **ENCORE** (Exploring Natural Capital Opportunities, Risks and Exposure)
   - Qualitative ratings of sector dependencies on ecosystem services
   - Example: Agriculture has "Very High" dependency on pollination

2. **EXIOBASE** (Multi-Regional Input-Output Database)
   - A matrix: Technical coefficients (sector inputs per unit output)
   - Z matrix: Inter-industry transactions
   - X vector: Total output per sector-country

3. **ND-GAIN** (Notre Dame Global Adaptation Initiative)
   - Country-level vulnerability indices for:
     - Ecosystems
     - Water resources
     - Habitat quality
     - Food security

**Process Flow:**
```
ENCORE Data → Load and clean dependency ratings → ISIC codes
                                                      ↓
                                              Map to NACE codes
                                                      ↓
EXIOBASE Data → Build Leontief inverse (L-I) → Calculate indirect dependencies
        ↓                                             ↓
Calculate SR (subcontracting ratio)          DS_direct × (L-I) = DS_indirect
                                                      ↓
ND-GAIN Data → PCA clustering of ES → Match to nature indices
        ↓                                             ↓
Apply nature degradation indices → Vuln = DS × Nature_Index
                                                      ↓
                                    Calculate for government/financial sectors
                                                      ↓
                            Output: Vuln_final.csv + Alpha_final.xlsx
```

**Key Calculations:**

1. **Direct Dependencies (DS_direct)**
   - From ENCORE: How directly a sector depends on an ecosystem service
   - Mapped from ISIC codes to EXIOBASE sectors

2. **Indirect Dependencies (DS_indirect)**
   - Calculated using Leontief inverse: `DS_indirect = DS_direct × (L-I)`
   - Captures supply chain dependencies

3. **Total Dependencies (DS_total)**
   - Option 1 (SR-weighted): `DS_total_SR = DS_indirect × SR + DS_direct × (1-SR)`
   - Option 2 (Max): `DS_total_max = max(DS_indirect, DS_direct)`

4. **Vulnerabilities (Vuln)**
   - `Vuln = DS × Nature_Degradation_Index`
   - Nature indices matched to ecosystem services via PCA clustering

5. **Alpha Shock Parameters**
   - `Alpha = Production_Shock / Weighted_Average_Vuln`
   - Converts vulnerability scores to scenario shock magnitudes

**Special Sector Handling:**

- **Government sector**: Calculated as production-weighted average of all sectors
- **Financial sector**: Calculated as asset-weighted average of non-financial sectors
  - Reflects indirect exposure through loan/investment portfolios

### How to Regenerate Vulnerability Files

**Method 1: Using the convenience function**
```python
import nature_analysis

# Regenerate from scratch (10-30 minutes)
shapes = nature_analysis.regenerate_vulnerability_files()

print(f"Generated Alpha file: {shapes['alpha']}")
print(f"Generated Vuln file: {shapes['vuln']}")
```

**Method 2: Using the example script**
```bash
python examples/vulnerability_generation.py
```

**Method 3: Direct module usage**
```python
from nature_analysis import vulnerability_generator
from pathlib import Path

# Run full generation workflow
path_ds_store = Path('data/DS_Vuln_update/')
shapes = vulnerability_generator.run_full_vulnerability_generation(path_ds_store)
```

### Configuration Requirements

**Centralized Configuration (`config.py`):**

All data paths and common parameters are centralized in `nature_analysis/config.py`:

```python
# ENCORE data
ENCORE_FILE = BASE_PATH / 'downloaded_data/ENCORE/06. Dependency mat ratings.csv'

# EXIOBASE data
EXIOBASE_PATH = BASE_PATH / 'downloaded_data/EXIOBASE 3/IOT_2022_ixi/IOT_2022_ixi'
EXIOBASE_A_MATRIX = EXIOBASE_PATH / 'A.csv'
EXIOBASE_Z_MATRIX = EXIOBASE_PATH / 'Z.csv'
EXIOBASE_X_VECTOR = EXIOBASE_PATH / 'x.csv'

# ISIC-NACE mapping
ISIC_NACE_MAPPING = BASE_PATH / 'downloaded_data/ENCORE/14. EXIOBASE NACE ISIC crosswalk.csv'

# ND-GAIN data
NATURE_INDEX_PATH = BASE_PATH / 'downloaded_data/ND-GAIN index/resources/vulnerability'
ISO_CODES_PATH = BASE_PATH / 'downloaded_data/Misc_tables'

# Configuration files directory
DS_VULN_UPDATE_PATH = BASE_PATH / 'DS_Vuln_update'
VULN_config_PATH = DS_VULN_UPDATE_PATH / 'config_store'

# Adjustment indicators
ADJ_IND_FILE = 'ROE_ROA_debt_ratio per NACE lvl1/Adj_ind_by_industry.xlsx'
AREA_COUNTRY_CODE_FILE = 'regions_ISO2_continent_area.csv'
```

**Scenario Configuration Files (`config_store/config_*.py`):**

Place scenario-specific configuration files in `DS_Vuln_update/config_store/`:
- `config_0_World_shock_10perc_02_GOVonNFC.py`
- `config_1_EUshock_3perc_08_GOVonNFC.py`
- etc.

Each scenario configuration file contains **ONLY scenario-specific parameters**:
- **ENCORE rating mapping** - Dependency rating conversion (linear/exponential/S-curve)
- **Production shocks** - Shock magnitudes per region (e.g., -0.1 for 10% shock)
- **Gov/NFC ratio** - Split between government and non-financial corporates
- **Activation flags** - Enable/disable alternative gov/financial vulnerability calculations

**Example scenario configuration:**
```python
"""Scenario: World shock 10% with Gov/NFC ratio 0.2"""
import pandas as pd

# ENCORE rating mapping (scenario-specific)
rating_mapping_linear = {'ND': 0, 'VL': 0.2, 'L': 0.4, 'M': 0.6, 'H': 0.8, 'VH': 1}
rating_mapping = rating_mapping_linear

# Production shock by region
data_shock = {
    "Area": ['European Union (EU)', 'North America', ...],
    "Production shock": [-0.1, -0.1, ...]  # 10% shock
}
data_shock = pd.DataFrame(data_shock)

# Government/NFC ratio
ratio_Gov_on_NFCpGov = 0.2

# Vulnerability calculation flags
activation_gov_vuln = 0
activation_fin_vuln = 0
```

**Key Improvement:** All data paths are now centralized in `config.py`, eliminating redundancy across scenario files. Scenario files are ~60% smaller and contain only parameters that vary between scenarios.

### Vulnerability Generator Module Functions

Key functions in `vulnerability_generator.py`:

**Data Loading:**
- `load_nd_gain_data()` - Load ND-GAIN vulnerability indices
- `load_and_clean_encore()` - Load ENCORE dependency ratings
- `create_isic_nace_mapping()` - Map ISIC to NACE codes

**Matrix Calculations:**
- `build_leontief_matrix()` - Compute Leontief inverse (L-I)
- `calculate_subcontracting_ratio()` - Calculate SR per sector

**Analysis:**
- `perform_pca_clustering()` - Cluster ecosystem services for nature index matching
- `merge_public_admin_vulnerability()` - Calculate government sector exposure
- `merge_financial_vulnerability()` - Calculate financial sector exposure

**Orchestration:**
- `generate_ds_file()` - Generate vulnerability file for one scenario
- `reshape_and_merge_ds_files()` - Merge all scenarios into final files
- `run_full_vulnerability_generation()` - Complete workflow for all scenarios
- `regenerate_vulnerability_files()` - Convenience function for package users

### Output Files

**Vuln_final.csv structure:**
```
region, EXIOBASE, eco_serv, indout, NACE Code, Adj_ind,
0_World_shock_10perc_DS_total_SR, 0_World_shock_10perc_DS_total_max,
0_World_shock_10perc_Vuln_total_SR, 0_World_shock_10perc_Vuln_total_max,
1_EUshock_15perc_DS_total_SR, ...
```

**Alpha_final.xlsx structure:**
```
Area, eco_serv,
0_World_shock_10perc_DS_total_SR_alpha, 0_World_shock_10perc_DS_total_max_alpha,
0_World_shock_10perc_Vuln_total_SR_alpha, 0_World_shock_10perc_Vuln_total_max_alpha,
1_EUshock_15perc_DS_total_SR_alpha, ...
```

### Standard Workflow (Using Pre-Generated Files)

**This is the recommended approach:**

```python
# Load pre-generated vulnerability data
from nature_analysis import AnalysisPipeline

pipeline = AnalysisPipeline()
pipeline.load_all_data()  # Loads Vuln_final.csv and Alpha_final.xlsx

# Calculate depreciation using stored vulnerabilities
depreciation_df = pipeline.calculate_instrument_depreciations()

# Apply financial models
impact_df = pipeline.calculate_financial_impacts(depreciation_df)

# Aggregate results
results = pipeline.calculate_shs_losses(impact_df)
```

See `examples/using_stored_vulnerabilities.py` for complete example.

### Key Differences: Standard vs. Regeneration Workflow

| Aspect | Standard Workflow | Regeneration Workflow |
|--------|-------------------|----------------------|
| **Input** | Vuln_final.csv, Alpha_final.xlsx | ENCORE, EXIOBASE, ND-GAIN raw data |
| **Time** | Minutes | 10-30 minutes |
| **Frequency** | Every analysis | Rarely (only when updating data) |
| **Output** | Portfolio losses | Vulnerability files |
| **Module** | `pipeline.py`, `vulnerability.py` | `vulnerability_generator.py` |
| **Example** | `using_stored_vulnerabilities.py` | `vulnerability_generation.py` |

### When to Regenerate

✅ **DO regenerate** when:
- New ENCORE data is released
- EXIOBASE updates to a new year
- ND-GAIN indices are updated
- Adding new scenario configurations
- Modifying shock parameters
- Changing government/financial sector calculation methods

❌ **DON'T regenerate** for:
- Regular portfolio analysis
- Different instrument datasets (SHS vs AnaCredit)
- Different holder data
- Visualization changes
- Financial model parameter adjustments

The vulnerability scores are **scenario-specific** but **instrument-agnostic**. They describe sector-country-ecosystem service relationships, not individual securities.

---

## Architecture Overview

### Data Flow

**SHS Pipeline (Securities Holdings):**
```
Input Files (CSV/Excel)
    ↓
[Data Loader] → load_SHS_data(), load_vulnerability_data(), load_alpha_data()
    ↓
SHS Instrument Data + Vulnerability Scores + Alpha Shocks + Holder Data
    ↓
[Vulnerability Calculator] → Parallel processing by (ecosystem service, scenario)
    ↓
Depreciation Matrix (instruments × scenarios)
    ↓
[Financial Models] → Apply Merton framework
    ↓
Financial Impacts (PD changes, LGD, price variations)
    ↓
[SHS Pipeline Aggregation] → Merge with holder data
    ↓
Final Results CSV (by holder, sector, geography, ecosystem service)
```

**AnaCredit Pipeline (Bank Lending):**
```
Input Files (CSV/Excel)
    ↓
[Data Loader] → load_Anacredit_data(), load_vulnerability_data(), load_alpha_data()
    ↓
AnaCredit Instrument Data + Vulnerability Scores + Alpha Shocks
    ↓
[Vulnerability Calculator] → Parallel processing by (ecosystem service, scenario)
    ↓
Depreciation Matrix (instruments × scenarios)
    ↓
[Financial Models] → Apply Merton framework
    ↓
Financial Impacts CSV (by instrument, ecosystem service, scenario)
```

### Module Responsibilities

| Module | Primary Purpose | Key Outputs |
|--------|----------------|-------------|
| `config.py` | Centralized parameters | Constants, paths (SHS & AnaCredit), settings, vulnerability generation params |
| `data_loader.py` | Load and preprocess data | DataFrames (SHS/AnaCredit instruments, vulnerability, alpha, holders) |
| `vulnerability_generator.py` | **[Optional]** Generate vulnerability files | Vuln_final.csv, Alpha_final.xlsx from ENCORE/EXIOBASE/ND-GAIN |
| `vulnerability.py` | Calculate depreciations | Depreciation matrix (instruments × scenarios) |
| `financial.py` | Financial modeling | PD, LGD, bond prices, equity prices |
| `pipeline.py` | Orchestration | Two pipeline classes (SHSAnalysisPipeline, AnaCreditAnalysisPipeline) |
| `visualization.py` | Plotting | Heatmaps, charts |

### Key Functions Reference

#### Data Loading (`data_loader.py`)
- `load_SHS_data()` - Load SHS financial instruments with risk metrics
- `load_Anacredit_data()` - Load AnaCredit (bank lending) instruments with risk metrics
- `load_vulnerability_data()` - Load ecosystem vulnerability scores
- `load_alpha_data()` - Load shock parameters
- `load_shs_holder_data()` - Load securities holdings (SHS only)
- `prepare_vulnerability_with_alpha()` - Merge vulnerability and shock data

#### Vulnerability Calculations (`vulnerability.py`)
- `calculate_depreciation()` - Main depreciation calculation for one scenario (SHS)
- `calculate_anacredit_depreciation()` - Depreciation calculation for AnaCredit (wrapper)
- `compute_weighted_metric()` - Production-weighted averaging across sectors
- `calculate_all_depreciations()` - Parallel processing wrapper for all scenarios (SHS)
- `calculate_all_anacredit_depreciations()` - Parallel processing wrapper for AnaCredit

**Note:** Despite having separate functions, the underlying calculation logic is identical.

#### Financial Models (`financial.py`)
- `pd_to_dd()` - Convert probability of default to distance to default
- `dd_to_pd()` - Convert distance to default to probability of default
- `calculate_asset_volatility()` - Derive asset volatility from equity volatility
- `calculate_lgd()` - Calculate loss given default with correlation
- `calculate_risky_bond_price()` - Price a credit-risky bond
- `calculate_bond_price_variation()` - Price change from PD shock
- `calculate_equity_price_variation()` - Equity price change (Merton model)

#### Pipeline (`pipeline.py`)
- `SHSAnalysisPipeline` class - Main orchestration for SHS data
  - `load_all_data()` - Load all required files (SHS instruments, vulnerability, alpha, NACE, holders)
  - `calculate_instrument_depreciations()` - Calculate depreciation matrix
  - `calculate_financial_impacts()` - Apply Merton model
  - `calculate_shs_losses()` - Aggregate portfolio losses by holder
  - `run_full_pipeline()` - Execute complete SHS workflow
  - `run_quick_test()` - Fast test with limited data

- `AnaCreditAnalysisPipeline` class - Main orchestration for AnaCredit data
  - `load_all_data()` - Load all required files (AnaCredit instruments, vulnerability, alpha, NACE)
  - `calculate_instrument_depreciations()` - Calculate depreciation matrix
  - `calculate_financial_impacts()` - Apply Merton model
  - `run_full_pipeline()` - Execute complete AnaCredit workflow

---

## Common Tasks and How to Approach Them

### Task: Add a New Financial Parameter

1. **Add to config.py**:
   ```python
   NEW_PARAMETER = 0.05  # Description
   ```

2. **Use in appropriate module** (likely `financial.py`):
   ```python
   from . import config

   def new_calculation():
       param = config.NEW_PARAMETER
       # ... use param
   ```

3. **Add test** in `tests/test_suite.py`:
   ```python
   def test_new_calculation():
       result = financial.new_calculation()
       assert abs(result - expected) < 1e-6
   ```

4. **Document** in README.md:
   - Add to Configuration section
   - Add to API Reference if it's a new function

### Task: Modify Data Loading

1. **Identify the loader function** in `data_loader.py`
   - For SHS: `load_SHS_data()`
   - For AnaCredit: `load_Anacredit_data()`
   - For shared data: `load_vulnerability_data()`, `load_alpha_data()`, etc.

2. **Understand current data structure** - read the function first
3. **Make minimal changes** - preserve existing columns unless necessary
4. **Test downstream effects** - check if both pipelines still work
5. **Update data requirements** in README.md if schema changes

### Task: Add Support for a New Data Source

If you need to add a third data source (e.g., "NewSource"):

1. **Add file path** to `config.py`:
   ```python
   NEWSOURCE_INSTRUMENT_FILE = '/path/to/newsource_data.csv'
   ```

2. **Add loader function** to `data_loader.py`:
   ```python
   def load_NewSource_data(file_path=config.NEWSOURCE_INSTRUMENT_FILE):
       return pd.read_csv(file_path, dtype={'nace': 'str'})
   ```

3. **Add wrapper functions** to `vulnerability.py`:
   ```python
   def calculate_newsource_depreciation(*args, **kwargs):
       return calculate_depreciation(*args, **kwargs)
   ```

4. **Create pipeline class** in `pipeline.py`:
   ```python
   class NewSourceAnalysisPipeline:
       # Similar structure to SHSAnalysisPipeline or AnaCreditAnalysisPipeline
   ```

5. **Export in __init__.py**:
   ```python
   from .pipeline import NewSourceAnalysisPipeline
   ```

6. **Document** in README.md

### Task: Change Financial Model

⚠️ **HIGH RISK** - Financial models are mathematically precise

1. **Understand the existing model** completely first
2. **Check academic literature** for the formula you're implementing
3. **Add detailed comments** explaining the math
4. **Add unit tests** with hand-calculated expected values
5. **Run full test suite** to check for regressions
6. **Document the change** thoroughly in code and README

### Task: Optimize Performance

1. **Profile first** - don't optimize without data:
   ```python
   import cProfile
   cProfile.run('pipeline.run_full_pipeline()', 'profile_stats')
   ```

2. **Common bottlenecks**:
   - Depreciation calculation (already parallelized)
   - Data merges (use efficient join strategies)
   - Repeated calculations (cache if appropriate)

3. **Optimization strategies**:
   - Use vectorized operations (NumPy/Pandas)
   - Leverage parallel processing (joblib)
   - Use efficient data types (categorical for strings)
   - Avoid unnecessary copies

### Task: Debug a Data Issue

1. **Check logs** - the code uses logging extensively

2. **Inspect intermediate DataFrames**:
   ```python
   # For SHS
   shs_pipeline = SHSAnalysisPipeline()
   shs_pipeline.load_all_data()
   print(shs_pipeline.instrmnt_df.head())
   print(shs_pipeline.instrmnt_df.info())

   # For AnaCredit
   anacredit_pipeline = AnaCreditAnalysisPipeline()
   anacredit_pipeline.load_all_data()
   print(anacredit_pipeline.instrmnt_df.head())
   print(anacredit_pipeline.instrmnt_df.info())
   ```

3. **Common issues**:
   - Missing NACE codes → Check NACE mapping files
   - Missing countries in alpha data → Check area mapping
   - NaN values → Check merge keys and data completeness
   - Performance issues → Check data volumes and parallelization
   - Wrong data source → Verify using correct pipeline (SHS vs AnaCredit)

4. **Validation checks**:
   ```python
   # Check for NaN values
   print(df.isnull().sum())

   # Check merge success
   print(f"Before merge: {len(df1)} rows")
   print(f"After merge: {len(merged)} rows")

   # Check data ranges
   print(df.describe())
   ```

---

## Critical Pitfalls to Avoid

### ❌ Breaking the Merton Model

**DON'T:**
- Modify PD/DD conversion formulas without understanding
- Change asset volatility calculation arbitrarily
- Remove correlation from LGD formula
- Alter bond pricing equations

**WHY:** These are precise mathematical implementations from academic literature. Changes will produce incorrect results.

**IF YOU NEED TO:** Consult financial literature first, document thoroughly, add validation tests.

### ❌ Ignoring NaN Values

**DON'T:**
- Assume NaN values will be handled automatically
- Drop rows without understanding why they're NaN
- Use `.fillna()` without justification

**WHY:** NaN values cascade through the pipeline and produce silent failures.

**DO:**
- Check for NaN values at each stage
- Log warnings when NaN values appear
- Investigate root cause (usually missing mapping data)

### ❌ Changing Configuration Defaults Without Understanding

**DON'T:**
- Change PD_CALIB, LGD_CALIB, or RISK_FREE_RATE arbitrarily
- Modify AGGREG_TYPE without understanding implications
- Change ECO_SERVICES list without verifying data availability
- Mix up SHS_INSTRUMENT_FILE and ANACREDIT_INSTRUMENT_FILE paths

**WHY:** These parameters are calibrated for specific analysis requirements.

**DO:**
- Ask about the purpose of the parameter
- Run sensitivity analysis to understand impact
- Document why you're changing it
- Verify you're using the correct data source for each pipeline

### ❌ Skipping Tests

**DON'T:**
- Consider a change complete without running tests
- Modify test tolerances to make tests pass
- Delete failing tests

**WHY:** Tests validate against known-good reference outputs. Failures indicate problems.

**DO:**
- Run `python tests/test_suite.py` after every change
- Investigate test failures thoroughly
- Update tests only when you understand why they fail and the new behavior is correct

### ❌ Premature Optimization

**DON'T:**
- Optimize code without profiling first
- Sacrifice readability for marginal performance gains
- Complicate code structure without measured benefit

**WHY:** Clarity is more valuable than speed until bottlenecks are proven.

**DO:**
- Profile to identify real bottlenecks
- Optimize hot paths only
- Preserve code clarity
- Measure before/after performance

### ❌ Confusing SHS and AnaCredit Pipelines

**DON'T:**
- Use `load_SHS_data()` for AnaCredit analysis or vice versa
- Expect holder aggregation in AnaCredit results
- Assume outputs are identical between pipelines

**WHY:** They serve different use cases with different data structures.

**DO:**
- Verify which data source you're working with
- Use the appropriate pipeline class
- Understand the output differences:
  - SHS: Portfolio losses by holder
  - AnaCredit: Financial impacts by instrument

---

## Financial Concepts Quick Reference

### Probability of Default (PD)
- **Definition**: Likelihood that a borrower will default within a given time period
- **Range**: 0 to 1 (0% to 100%)
- **Typical values**: 0.01 to 0.10 for most firms (1% to 10%)

### Distance to Default (DD)
- **Definition**: Number of standard deviations between current asset value and default threshold
- **Range**: Typically -3 to +5
- **Relationship**: DD = -Φ⁻¹(PD), where Φ is cumulative normal distribution

### Loss Given Default (LGD)
- **Definition**: Expected loss if default occurs
- **Range**: 0 to 1 (0% to 100%)
- **Typical values**: 0.40 to 0.70 (40% to 70% loss)

### Asset Volatility (σ_V)
- **Definition**: Standard deviation of firm asset returns
- **Derived from**: Equity volatility using Merton model
- **Typical values**: 0.10 to 0.50 (10% to 50% annual volatility)

### Ecosystem Service Depreciation
- **Definition**: Percentage decline in firm assets due to ecosystem disruption
- **Mechanism**: Ecosystem shock → Production decline → Asset value falls
- **Range**: Typically 0% to 5% for most scenarios

### Merton Structural Model
- **Key insight**: Equity is a call option on firm assets
- **Default occurs**: When asset value falls below debt at maturity
- **Applications**: Credit risk modeling, equity valuation

---

## Data Sources: SHS vs AnaCredit

### Securities Holdings Statistics (SHS)

**What it is:**
- Financial instruments held by institutional investors
- Bonds, equities, and other securities
- Includes holder information (who owns what)

**Pipeline:**
- Class: `SHSAnalysisPipeline`
- Loader: `load_SHS_data()`
- Holder data: `load_shs_holder_data()`

**Output:**
- Portfolio losses aggregated by:
  - Holder sector (e.g., Financial Corps, Government)
  - Holder geography (e.g., NL, DE, FR)
  - Ecosystem service
  - Scenario

**Use case:**
- Assessing nature-related financial risks for pension funds, insurance companies, investment funds

### AnaCredit (Analytical Credit Datasets)

**What it is:**
- Bank lending data
- Loans to non-financial corporations
- Direct instrument-level data (no holder aggregation)

**Pipeline:**
- Class: `AnaCreditAnalysisPipeline`
- Loader: `load_Anacredit_data()`
- No holder data needed

**Output:**
- Financial impacts by:
  - Instrument (ISIN)
  - Ecosystem service
  - Scenario
- Includes: PD changes, LGD, price variations

**Use case:**
- Assessing nature-related credit risks in bank loan portfolios

### Key Differences

| Aspect | SHS | AnaCredit |
|--------|-----|-----------|
| **Data type** | Securities holdings | Bank lending |
| **Instruments** | Bonds, equities | Loans |
| **Holder data** | ✅ Required | ❌ Not applicable |
| **Final aggregation** | By holder sector/geography | By instrument only |
| **Pipeline class** | `SHSAnalysisPipeline` | `AnaCreditAnalysisPipeline` |
| **Config path** | `SHS_INSTRUMENT_FILE` | `ANACREDIT_INSTRUMENT_FILE` |
| **Loader function** | `load_SHS_data()` | `load_Anacredit_data()` |
| **Depreciation function** | `calculate_depreciation()` | `calculate_anacredit_depreciation()` |
| **Batch processing** | `calculate_all_depreciations()` | `calculate_all_anacredit_depreciations()` |

### Shared Components

Both pipelines use the same:
- Vulnerability data (`load_vulnerability_data()`)
- Alpha shock data (`load_alpha_data()`)
- NACE mapping (`load_nace_mapping()`)
- Production data (`load_production_data()`)
- Financial models (Merton framework)
- **Core calculation logic** (identical depreciation formulas)

---

## Code Style and Patterns

### Error Handling

```python
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process data with validation."""
    # Validate inputs
    required_cols = ['ISIN', 'PD', 'vol']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Handle edge cases
    if df.empty:
        logger.warning("Empty DataFrame, returning empty result")
        return pd.DataFrame()

    # Main logic
    try:
        result = perform_calculation(df)
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        raise

    return result
```

### Logging Pattern

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed diagnostic info")
logger.info("Progress information")
logger.warning("Unexpected but handled")
logger.error("Error preventing operation")
```

### Type Hints

```python
from typing import Tuple, List
import pandas as pd

def calculate_metric(
    data: pd.DataFrame,
    weight_col: str,
    value_col: str,
    threshold: float = 0.5
) -> Tuple[float, pd.DataFrame]:
    """
    Calculate weighted metric.

    Args:
        data: Input DataFrame
        weight_col: Column name for weights
        value_col: Column name for values
        threshold: Minimum threshold (default: 0.5)

    Returns:
        Tuple of (metric value, filtered DataFrame)
    """
    ...
```

### Docstring Format (Google Style)

```python
def complex_function(param1: float, param2: str) -> pd.DataFrame:
    """
    One-line summary of what the function does.

    Longer description if needed. Explain algorithm, assumptions,
    or important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
    ...
```

---

## Testing Strategy

### Unit Tests
Test individual functions in isolation:
```python
def test_pd_to_dd():
    """Test PD to DD conversion."""
    dd = financial.pd_to_dd(pd=0.05)
    assert abs(dd - 1.645) < 0.01
```

### Integration Tests
Test complete workflows:
```python
def test_shs_pipeline():
    """Test complete SHS analysis pipeline."""
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)
    assert len(results) > 0
    assert 'VALUE_LOSS' in results.columns

def test_anacredit_pipeline():
    """Test complete AnaCredit analysis pipeline."""
    pipeline = AnaCreditAnalysisPipeline()
    results = pipeline.run_full_pipeline()
    assert len(results) > 0
    assert 'ISIN' in results.columns
```

### Validation Tests
Compare against reference outputs:
```python
def test_output_matches_reference():
    """Compare outputs with known-good reference."""
    reference_df = pd.read_csv('reference_output.csv')
    pipeline = SHSAnalysisPipeline()
    new_df = pipeline.run_full_pipeline()
    assert np.allclose(reference_df['VALUE_LOSS'],
                      new_df['VALUE_LOSS'],
                      rtol=0.01)
```

---

## When to Ask for Clarification

Ask the user for clarification when:

1. **Financial formula changes** - These affect real-world risk calculations
2. **Parameter calibration** - PD_CALIB, LGD_CALIB have specific meanings
3. **Data schema changes** - May affect downstream systems
4. **Test failures** - Could indicate real problems
5. **Performance trade-offs** - Speed vs. clarity decisions
6. **Ecosystem service definitions** - Domain-specific terminology
7. **Aggregation methods** - 'SR' vs 'max' have specific implications
8. **Data source selection** - When unclear whether to use SHS or AnaCredit
9. **New data source addition** - Architecture decisions needed

---

## Useful Commands

```bash
# Quick test (fast - use this first!)
python -c "import nature_analysis; nature_analysis.run_quick_test(n_instruments=10)"

# Quick test for AnaCredit
python -c "import nature_analysis; nature_analysis.run_anacredit_quick_test(n_instruments=10)"

# Run quick test examples
python examples/quick_test.py

# Run SHS examples
python examples/basic_usage.py

# Run AnaCredit examples
python examples/anacredit_usage.py

# Run full test suite
python tests/test_suite.py

# Quick validation
python tests/quick_compare.py

# Test imports
python tests/test_import.py

# Check package structure
python -c "import nature_analysis; print(dir(nature_analysis))"

# Profile performance (SHS)
python -m cProfile -o profile.stats examples/basic_usage.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"

# Profile performance (AnaCredit)
python -m cProfile -o profile.stats examples/anacredit_usage.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"
```

---

## Summary: Your Workflow

1. **Understand the request** - What's the goal? Which data source (SHS or AnaCredit)?
2. **Read relevant code** - Don't modify blindly
3. **Check configuration** - What parameters are set? Which paths are used?
4. **Choose the right pipeline** - SHSAnalysisPipeline or AnaCreditAnalysisPipeline?
5. **Make minimal changes** - Preserve existing functionality
6. **Add logging** - Help future debugging
7. **Write tests** - Validate your changes for both pipelines if applicable
8. **Run test suite** - Check for regressions
9. **Document changes** - Update README.md if needed
10. **Explain your changes** - Help the user understand what you did

---

## Contact and Escalation

If you encounter:
- **Mathematical questions** about financial models → Ask user for clarification
- **Domain-specific questions** about ecosystem services → Ask user
- **Data availability issues** → Check with user about data sources
- **Conflicting requirements** → Ask user to prioritize
- **Uncertainty about SHS vs AnaCredit** → Ask user which analysis they need

---

**Remember**: This code handles real financial data for central banks. Precision and correctness are more important than speed or cleverness.

---

**Last Updated**: 2025-11-18
**For**: Claude and other AI assistants
**Version**: 2.0.0
