# Nature-Based Financial Risk Analysis

> **A production-ready Python package for quantifying how ecosystem service disruptions impact financial portfolios through credit risk modeling**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Data Requirements](#data-requirements)
- [Financial Models](#financial-models)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🌍 Overview

### What This Package Does

This system quantifies how disruptions to **ecosystem services** (e.g., water regulation, pollination, soil retention) propagate through the economy to affect **financial portfolios**. It combines:

1. **Ecosystem Science**: Vulnerability of economic sectors to nature degradation
2. **Financial Theory**: Merton structural model for credit risk
3. **Portfolio Analysis**: Support for multiple data sources (SHS and AnaCredit)

**Key Output**: Portfolio value losses aggregated by holder, sector, geography, and ecosystem service scenario.

### Key Features

- ✅ Calculate asset depreciation from ecosystem service disruptions
- ✅ Model financial impacts using Merton credit risk framework
- ✅ **Support for multiple data sources**: Securities Holdings Statistics (SHS) and AnaCredit
- ✅ Aggregate portfolio losses across multiple dimensions
- ✅ Support for multiple scenarios and ecosystem services
- ✅ Parallel processing for performance
- ✅ Comprehensive testing and validation
- ✅ Professional package structure with clean API

### What's New in v2.0

- 🎯 **Dual data source support**: Separate pipelines for SHS (securities holdings) and AnaCredit (bank lending)
- 📁 **Professional structure**: Organized into `nature_analysis/`, `tests/`, `examples/`, `legacy/`
- 📦 **Easy installation**: Proper `setup.py` with pip install support
- 📚 **Better documentation**: Clear input/output specifications and examples for both data sources
- 🔧 **Cleaner API**: Dedicated pipeline classes (`SHSAnalysisPipeline`, `AnaCreditAnalysisPipeline`)
- 🗂️ **Explicit data loaders**: Separate functions for SHS vs AnaCredit data

### Data Sources

The package supports two types of financial data:

| Data Source | Description | Use Case | Output |
|-------------|-------------|----------|--------|
| **SHS** | Securities Holdings Statistics | Portfolio risk for institutional holders (e.g., pension funds, insurance) | Portfolio losses by holder sector/geography |
| **AnaCredit** | Analytical Credit Datasets | Credit risk for bank loan portfolios | Financial impacts by instrument |

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/reoptimus/nature_paper_DNB.git
cd nature_paper_DNB

# Install in editable mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

### Dependencies

- **pandas** (>=1.3.0) - Data manipulation
- **numpy** (>=1.20.0) - Numerical computing
- **scipy** (>=1.7.0) - Scientific computing
- **matplotlib** (>=3.4.0) - Plotting
- **seaborn** (>=0.11.0) - Statistical visualizations
- **joblib** (>=1.0.0) - Parallel processing
- **openpyxl** (>=3.0.0) - Excel file support

---

## 🚀 Quick Start

### Example 0: Quick Test (Fast & Lightweight) ⚡

**Perfect for testing, demos, or first-time users!**

```python
import nature_analysis

# SHS quick test - Run with only 100 instruments, 1 scenario, 1 ecosystem service
results = nature_analysis.run_quick_test(n_instruments=100)

print(f"Quick test complete! Processed {len(results)} instruments")
print(f"Depreciation column: {results.columns[-1]}")
```

**Output:**
```
Quick test complete! Processed 100 instruments
Depreciation column: Depr_1_World_shock_10perc_02_GOVonNFC_Soil and sediment retention
```

**⏱️ Speed:** ~10-30 seconds (vs. 10-30 minutes for full pipeline)

### Example 1: One-Line Execution (SHS)

```python
import nature_analysis

# Run complete SHS analysis with default settings
results = nature_analysis.run_pipeline()

print(f"Analysis complete!")
print(f"Total portfolio value: €{results['OBS_VALUE'].sum():,.0f}")
print(f"Total value loss: €{results['VALUE_LOSS'].sum():,.0f}")
print(f"Loss rate: {(results['VALUE_LOSS'].sum() / results['OBS_VALUE'].sum() * 100):.2f}%")
```

**Output:**
```
Analysis complete!
Total portfolio value: €5,234,891,234
Total value loss: €45,678,912
Loss rate: 0.87%
```

### Example 2: AnaCredit Analysis

```python
import nature_analysis

# Run AnaCredit analysis (bank lending portfolios)
results = nature_analysis.run_anacredit_pipeline()

print(f"AnaCredit analysis complete!")
print(f"Processed {len(results)} loan instruments")
print(f"Columns: {list(results.columns)}")
```

### Example 3: Using Pipeline Classes Directly

```python
from nature_analysis import SHSAnalysisPipeline, AnaCreditAnalysisPipeline

# SHS Pipeline
shs_pipeline = SHSAnalysisPipeline()
shs_results = shs_pipeline.run_full_pipeline(create_plots=True)
print(f"SHS: {len(shs_results)} portfolio loss records")

# AnaCredit Pipeline
anacredit_pipeline = AnaCreditAnalysisPipeline()
anacredit_results = anacredit_pipeline.run_full_pipeline()
print(f"AnaCredit: {len(anacredit_results)} instrument impact records")
```

### Example 4: Step-by-Step Analysis (SHS)

```python
from nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()

# Step 1: Load all data
pipeline.load_all_data()
print(f"✓ Loaded {len(pipeline.instrmnt_df)} instruments")
print(f"✓ Loaded {len(pipeline.vuln_df)} vulnerability records")

# Step 2: Calculate depreciations
depreciation_df = pipeline.calculate_instrument_depreciations()
print(f"✓ Calculated depreciations: {depreciation_df.shape}")

# Step 3: Calculate financial impacts
financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)
print(f"✓ Calculated financial impacts: {financial_impacts.shape}")

# Step 4: Calculate portfolio losses (SHS only)
results = pipeline.calculate_shs_losses(financial_impacts)
print(f"✓ Final results: {results.shape}")
```

---

## 📁 Project Structure

```
nature_paper_DNB/
├── README.md                   # This file
├── setup.py                    # Package installation script
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
├── CLAUDE.md                   # Guide for AI assistants
│
├── nature_analysis/            # Main package ⭐
│   ├── __init__.py            # Package initialization & exports
│   ├── config.py              # Configuration parameters
│   ├── data_loader.py         # Data loading & preprocessing
│   ├── vulnerability.py       # Vulnerability calculations
│   ├── financial.py           # Financial models (Merton, pricing)
│   ├── pipeline.py            # Main orchestration pipelines
│   └── visualization.py       # Plotting functions
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_suite.py          # Comprehensive validation tests
│   ├── quick_compare.py       # Fast output comparison
│   └── test_import.py         # Import validation
│
├── examples/                   # Usage examples
│   ├── __init__.py
│   ├── quick_test.py          # Fast testing examples ⚡
│   ├── basic_usage.py         # SHS examples
│   └── anacredit_usage.py     # AnaCredit examples
│
├── data/                       # Reference data
│   ├── NACE_mapping.csv       # NACE to EXIOBASE mapping
│   ├── region_mapping.csv     # Region mapping
│   └── ...                    # Other reference files
│
└── legacy/                     # Original reference code
    ├── __init__.py
    └── SHS_process.py         # Original implementation
```

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `config.py` | Centralized configuration | Constants, file paths, parameters |
| `data_loader.py` | Load and preprocess data | `load_SHS_data()`, `load_Anacredit_data()`, `load_vulnerability_data()` |
| `vulnerability.py` | Calculate depreciations | `calculate_depreciation()`, `calculate_anacredit_depreciation()`, `compute_weighted_metric()` |
| `financial.py` | Implement financial models | `calculate_lgd()`, `calculate_bond_price_variation()` |
| `pipeline.py` | Orchestrate workflow | `SHSAnalysisPipeline`, `AnaCreditAnalysisPipeline` classes |
| `visualization.py` | Generate plots | `plot_loss_heatmap_by_dimension()` |

---

## 💡 Usage Examples

### Analyze Specific Scenario (SHS)

```python
from nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=False)

# Analyze Water flow regulation impacts
water_results = results[results['Eco_serv'] == 'Water flow regulation']

print(f"\nWater Regulation Impacts:")
print(f"Total loss: €{water_results['VALUE_LOSS'].sum():,.0f}")
print(f"Affected value: €{water_results['OBS_VALUE'].sum():,.0f}")

# Group by holder sector
by_sector = water_results.groupby('HOLDER_SECTOR').agg({
    'VALUE_LOSS': 'sum',
    'OBS_VALUE': 'sum'
})
by_sector['Loss_Rate_%'] = (by_sector['VALUE_LOSS'] / by_sector['OBS_VALUE'] * 100)
print("\nLosses by Sector:")
print(by_sector)
```

**Output:**
```
Water Regulation Impacts:
Total loss: €12,345,678
Affected value: €1,234,567,890

Losses by Sector:
                     VALUE_LOSS    OBS_VALUE  Loss_Rate_%
HOLDER_SECTOR
Financial Corps      8,234,567   890,123,456         0.93
Government           2,111,111   234,444,434         0.90
Households           2,000,000   110,000,000         1.82
```

### Compare SHS vs AnaCredit Results

```python
from nature_analysis import SHSAnalysisPipeline, AnaCreditAnalysisPipeline

# Run both pipelines
shs_pipeline = SHSAnalysisPipeline()
shs_results = shs_pipeline.run_full_pipeline(create_plots=False)

anacredit_pipeline = AnaCreditAnalysisPipeline()
anacredit_results = anacredit_pipeline.run_full_pipeline()

# Compare
print(f"\nSHS Analysis:")
print(f"  Total instruments: {shs_pipeline.instrmnt_df['ISIN'].nunique()}")
print(f"  Total portfolio value: €{shs_results['OBS_VALUE'].sum():,.0f}")
print(f"  Total losses: €{shs_results['VALUE_LOSS'].sum():,.0f}")

print(f"\nAnaCredit Analysis:")
print(f"  Total loan instruments: {anacredit_pipeline.instrmnt_df['ISIN'].nunique()}")
print(f"  Columns: {list(anacredit_results.columns)}")
print(f"  Note: AnaCredit output contains financial impacts, not portfolio aggregations")
```

### Custom Visualization

```python
from nature_analysis import visualization, SHSAnalysisPipeline

# Run SHS pipeline
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=False)

# Create heatmap of losses by sector and geography
fig = visualization.plot_loss_heatmap_by_dimension(
    results_df=results,
    eco_service='Pollination',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    dimension_x='HOLDER_SECTOR',
    dimension_y='HOLDER_AREA',
    value_type='percentage',
    output_path='pollination_heatmap.png'
)

print("Visualization saved to pollination_heatmap.png")
```

### Sensitivity Analysis

```python
from nature_analysis import config, SHSAnalysisPipeline
import pandas as pd

# Test different PD calibrations
pd_values = [0.03, 0.0459, 0.06]
sensitivity_results = []

for pd_calib in pd_values:
    # Temporarily modify config
    original_pd = config.PD_CALIB
    config.PD_CALIB = pd_calib

    # Run analysis
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)

    # Store summary
    sensitivity_results.append({
        'PD_CALIB': pd_calib,
        'Total_Loss': results['VALUE_LOSS'].sum(),
        'Total_Value': results['OBS_VALUE'].sum(),
        'Loss_Rate_%': results['VALUE_LOSS'].sum() / results['OBS_VALUE'].sum() * 100
    })

    # Restore config
    config.PD_CALIB = original_pd

# Display sensitivity analysis
sensitivity_df = pd.DataFrame(sensitivity_results)
print(sensitivity_df)
```

**Output:**
```
   PD_CALIB    Total_Loss    Total_Value  Loss_Rate_%
0      0.03  32,145,234  5,234,891,234         0.614
1    0.0459  45,678,912  5,234,891,234         0.873
2      0.06  56,234,123  5,234,891,234         1.074
```

---

## ⚡ Performance: Quick Test vs Full Pipeline

### When to Use Quick Test

The `run_quick_test()` function is ideal for:

- **✓ Testing installation** - Verify everything works without waiting
- **✓ Development & debugging** - Quickly test changes
- **✓ Demos & presentations** - Show the workflow in real-time
- **✓ Learning the package** - Understand outputs without long waits
- **✓ Parameter exploration** - Test different configurations rapidly

### When to Use Full Pipeline

The `run_pipeline()` (SHS) or `run_anacredit_pipeline()` (AnaCredit) should be used for:

- **✓ Production analysis** - Complete portfolio risk assessment
- **✓ Final results** - All instruments, scenarios, and ecosystem services
- **✓ Reporting** - Comprehensive output with visualizations
- **✓ Research** - Full dataset analysis for papers/reports

### Performance Comparison

| Aspect | Quick Test | Full SHS Pipeline | Full AnaCredit Pipeline |
|--------|-----------|------------------|------------------------|
| **Instruments** | 100 (customizable) | ~50,000 | Varies by dataset |
| **Scenarios** | 1 (first) | All (~10-20) | All (~10-20) |
| **Ecosystem Services** | 1 (first) | All (6) | All (6) |
| **Runtime** | ~10-30 seconds | ~10-30 minutes | ~10-30 minutes |
| **Output** | Depreciation matrix | Portfolio losses by holder | Financial impacts by instrument |
| **Use Case** | Testing, demos | Institutional portfolio analysis | Bank lending portfolio analysis |

### Example Usage Comparison

**Quick Test:**
```python
import nature_analysis

# Fast: Only 100 instruments, 1 scenario, 1 ES
results = nature_analysis.run_quick_test(n_instruments=100)
# Runtime: ~20 seconds
```

**Full SHS Pipeline:**
```python
import nature_analysis

# Complete: All instruments, all scenarios, all ES
results = nature_analysis.run_pipeline()
# Runtime: ~15-30 minutes
```

**Full AnaCredit Pipeline:**
```python
import nature_analysis

# Complete: All loan instruments, all scenarios, all ES
results = nature_analysis.run_anacredit_pipeline()
# Runtime: ~15-30 minutes
```

### Running Example Scripts

```bash
# Run quick test examples
python examples/quick_test.py

# Run SHS examples
python examples/basic_usage.py

# Run AnaCredit examples
python examples/anacredit_usage.py
```

---

## ⚙️ Configuration

### Key Parameters

Edit `nature_analysis/config.py` to customize analysis:

```python
# Financial parameters
RISK_FREE_RATE = 0.02          # Annual risk-free rate (2%)
CORRELATION_RHO = 0.1          # Asset correlation (10%)
PD_CALIB = 0.0459             # Calibration probability of default
LGD_CALIB = 0.652             # Calibration loss given default

# Analysis settings
MAX_MATURITY = 30              # Maximum bond maturity (years)
AGGREG_TYPE = 'SR'            # Aggregation type: 'SR' or 'max'
DEPENDENCY_TYPE = 'Vuln_total' # Dependency metric type

# Ecosystem services to analyze
ECO_SERVICES = [
    'Soil and sediment retention',
    'Water purification',
    'Water flow regulation',
    'Pollination',
    'Climate regulation',
    'Pest and disease control',
]

# Country list
COUNTRIES = [
    'NL', 'AT', 'BE', 'DE', 'ES', 'FI', 'FR', 'GR',
    'HR', 'IT', 'PL', 'PT', 'US', 'JP', 'CN', 'CA'
]
```

### File Paths

Configure data file locations in `config.py`:

```python
from pathlib import Path

# Base paths
BASE_PATH = Path('I:/FS/FS/Statsp/000-Beleidsmedewerkers/Sebastien Gallet/Biodiv/OS-2025')
DATA_PATH = BASE_PATH / 'git_repo/nature_paper_DNB/data'
VULN_PATH = BASE_PATH / 'DS_Vuln_update/Vuln_final_store'
ANALYSIS_PATH = BASE_PATH / 'analysis/output_data'
RESULTS_PATH = Path('./results')  # Local output

# Input files in secured environment
# SHS instrument data
SHS_INSTRUMENT_FILE = 'G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/SHS/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'

# AnaCredit instrument data
ANACREDIT_INSTRUMENT_FILE = 'G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/anacredit_NL/anacredit_df_2024-12-31.csv'

# Shared data files
VULN_FILE = 'vuln_v2.csv'
ALPHA_FILE = 'alpha_DNB_dec2024.xlsx'
SHS_HOLDER_FILE = 'G:/FS/IFA/Sebastien/Nature 3.0/Nature_analysis/SHS/F_511_31_32_holdng_nature_2024-Q4.csv'
```

**Note:** The paths point to secured drives (G:/, H:/, I:/) in the DNB environment. Update these paths for your environment.

---

## 🔄 Vulnerability Data Generation (Optional)

### Two Workflows

The package supports two workflows for handling vulnerability data:

| Workflow | Description | Time | When to Use |
|----------|-------------|------|-------------|
| **Standard** (Recommended) | Use pre-generated `Vuln_final.csv` and `Alpha_final.xlsx` | Minutes | Regular portfolio analysis |
| **Regeneration** (Optional) | Generate vulnerability files from ENCORE/EXIOBASE/ND-GAIN | 10-30 min | Updating underlying vulnerability data |

**💡 Key Advantage:** Vulnerability generation is **completely independent** of financial analysis. You can:
- ✅ Generate vulnerability tables without any SHS or AnaCredit instrument data
- ✅ Test different scenario configurations (5%, 10%, 15% shocks) separately
- ✅ Update to new ENCORE/EXIOBASE releases without re-processing portfolios
- ✅ Create custom shock parameters for research purposes

This separation means vulnerability scores are **scenario-specific** but **instrument-agnostic** – they describe sector-country-ecosystem relationships, not individual securities.

**Example:** Run `python examples/vulnerability_generation.py` to generate vulnerability tables independently, then use them with any instrument dataset.

### Standard Workflow: Using Pre-Generated Files

**This is the recommended approach** for regular analysis:

```python
import nature_analysis

# Use pre-generated vulnerability files (stored in data directory)
results = nature_analysis.run_pipeline()

# Or for AnaCredit
results = nature_analysis.run_anacredit_pipeline()
```

The vulnerability files (`Vuln_final.csv` and `Alpha_final.xlsx`) contain sector-level vulnerability scores that are **scenario-specific** but **instrument-agnostic**. They can be reused across different instrument datasets (SHS or AnaCredit).

### Regeneration Workflow: Creating New Vulnerability Files

**Only regenerate vulnerability files when:**
- ✅ New ENCORE dependency ratings are released
- ✅ EXIOBASE updates to a new version/year
- ✅ ND-GAIN indices are updated
- ✅ Adding new scenario configurations
- ✅ Modifying shock parameters

**Don't regenerate for:**
- ❌ Different instrument datasets (SHS vs AnaCredit)
- ❌ Different holder data
- ❌ Financial model parameter changes
- ❌ Visualization adjustments

### How to Regenerate Vulnerability Files

**Method 1: Using the convenience function**

```python
import nature_analysis

# Regenerate from ENCORE, EXIOBASE, and ND-GAIN raw data
shapes = nature_analysis.regenerate_vulnerability_files()

print(f"Generated Alpha file: {shapes['alpha']}")
print(f"Generated Vuln file: {shapes['vuln']}")
```

**Method 2: Using the example script**

```bash
python examples/vulnerability_generation.py
```

**Method 3: See detailed example**

```bash
python examples/using_stored_vulnerabilities.py
```

### What Gets Generated

**Input Data Sources:**
1. **ENCORE** - Ecosystem service dependency ratings by sector
2. **EXIOBASE** - Multi-regional input-output matrices (A, Z, X)
3. **ND-GAIN** - Nature degradation vulnerability indices by country

**Process:**
```
ENCORE (sector dependencies)
    + EXIOBASE (economic linkages)
    + ND-GAIN (nature degradation)
    ↓
Calculate direct + indirect dependencies
    ↓
Apply nature degradation indices
    ↓
Generate vulnerability scores
    ↓
Vuln_final.csv + Alpha_final.xlsx
```

**Output Files:**
- `Vuln_final.csv` - Vulnerability scores per region/sector/ecosystem service/scenario
- `Alpha_final.xlsx` - Shock parameters per area/ecosystem service/scenario

### Configuration Requirements

**Centralized paths** are defined in `nature_analysis/config.py`:

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
```

**Scenario-specific parameters** are in `DS_Vuln_update/config_store/config_*.py`:
- `config_0_World_shock_10perc_02_GOVonNFC.py` - Contains only scenario-specific parameters
- `config_1_EUshock_3perc_08_GOVonNFC.py` - Production shocks, rating mappings, activation flags
- etc.

Each scenario file contains ONLY: rating mapping, production shocks, gov/NFC ratio, and activation flags.

### API Reference

**vulnerability_generator Module:**

```python
from nature_analysis import vulnerability_generator

# Load and process ENCORE data
encore_df = vulnerability_generator.load_and_clean_encore(
    path_to_file, rating_mapping
)

# Build Leontief inverse matrix
L_I_bar, A = vulnerability_generator.build_leontief_matrix(
    exiobase_a_matrix_path
)

# Calculate subcontracting ratios
SR_mat, X = vulnerability_generator.calculate_subcontracting_ratio(
    Z_path, X_path, list_cntry_sect
)

# Run full generation workflow
shapes = vulnerability_generator.run_full_vulnerability_generation(
    path_ds_store
)
```

See [`CLAUDE.md`](CLAUDE.md#vulnerability-data-generation-optional-workflow) for detailed documentation on the vulnerability generation workflow.

---

## 📊 Data Requirements

### Required Input Files

| File | Description | Key Columns | Used By |
|------|-------------|-------------|---------|
| **SHS Instrument Data** | Securities holdings statistics instruments | `ISIN`, `PD`, `vol`, `debt_ratio`, `nace`, `ISSUER_COUNTRY` | SHS Pipeline |
| **AnaCredit Instrument Data** | Bank lending data | `ISIN`, `PD`, `vol`, `debt_ratio`, `nace`, `ISSUER_COUNTRY` | AnaCredit Pipeline |
| **Vulnerability Scores** | Ecosystem service vulnerability by sector/region | `region`, `eco_serv`, `EXIOBASE`, `NACE Code`, `Vuln`, `Adj_ind` | Both |
| **Alpha Shocks** | Ecosystem service shock parameters | `Area`, `eco_serv`, various vulnerability types | Both |
| **SHS Holder Data** | Securities holdings by holder | `ISIN`, `HOLDER_SECTOR`, `HOLDER_AREA`, `OBS_VALUE` | SHS Pipeline only |
| **NACE Mapping** | NACE to EXIOBASE sector mapping | `NACE Code`, `EXIOBASE` | Both |
| **Production Data** | EXIOBASE production volumes | `Area`, `EXIOBASE`, `production` | Both |

### Data Source Differences

| Aspect | SHS Data | AnaCredit Data |
|--------|----------|----------------|
| **Source** | Securities holdings statistics | Analytical credit datasets (bank lending) |
| **Instrument Type** | Securities (bonds, equities) | Loans |
| **Holder Data** | ✅ Yes - Required for portfolio aggregation | ❌ No - Direct instrument analysis |
| **Final Output** | Portfolio losses by holder sector/geography | Financial impacts by instrument |
| **Pipeline Class** | `SHSAnalysisPipeline` | `AnaCreditAnalysisPipeline` |
| **Loader Function** | `load_SHS_data()` | `load_Anacredit_data()` |

### Data Validation

```python
from nature_analysis import SHSAnalysisPipeline, AnaCreditAnalysisPipeline

# Validate SHS data
shs_pipeline = SHSAnalysisPipeline()
shs_pipeline.load_all_data()

print(f"SHS Instruments: {len(shs_pipeline.instrmnt_df)} rows")
print(f"  Columns: {list(shs_pipeline.instrmnt_df.columns)}")
print(f"\nVulnerabilities: {len(shs_pipeline.vuln_df)} rows")
print(f"  Ecosystem services: {shs_pipeline.vuln_df['eco_serv'].nunique()}")

# Validate AnaCredit data
anacredit_pipeline = AnaCreditAnalysisPipeline()
anacredit_pipeline.load_all_data()

print(f"\nAnaCredit Instruments: {len(anacredit_pipeline.instrmnt_df)} rows")
print(f"  Columns: {list(anacredit_pipeline.instrmnt_df.columns)}")
```

---

## 💰 Financial Models

### Merton Structural Model Overview

The package implements the Merton structural credit risk model, which treats equity as a call option on firm assets.

**Key Insight**: Default occurs when asset value falls below debt at maturity.

#### Key Functions

```python
from nature_analysis import financial

# 1. Distance to Default
dd = financial.pd_to_dd(pd=0.05)  # Input: PD (0-1) → Output: DD (float)

# 2. Asset Volatility
sigma = financial.calculate_asset_volatility(dd=1.645, vol=0.30, debt_ratio=0.60)

# 3. Loss Given Default
lgd = financial.calculate_lgd(pd=0.05)  # Output: LGD (0-1)

# 4. Bond Pricing
price = financial.calculate_risky_bond_price(duration=5.0, pd=0.05, lgd=0.65)

# 5. Price Impact
variation = financial.calculate_bond_price_variation(duration=5.0, pd=0.05, lgd=0.65, delta_pd=0.01)
```

### Financial Concepts Quick Reference

- **PD (Probability of Default)**: Likelihood of default (0-1, typically 0.01-0.10)
- **DD (Distance to Default)**: Standard deviations to default (typically -3 to +5)
- **LGD (Loss Given Default)**: Expected loss if default occurs (0-1, typically 0.40-0.70)
- **Asset Volatility (σ_V)**: Standard deviation of firm asset returns (typically 0.10-0.50)
- **Ecosystem Depreciation**: Asset value decline from ecosystem disruption (typically 0%-5%)

---

## 📖 API Reference

### Main Classes

#### `SHSAnalysisPipeline`

```python
from nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
```

**Methods:**
- `load_all_data()` - Load SHS instruments, vulnerability, alpha, NACE mapping, holder data
- `calculate_instrument_depreciations()` - Calculate depreciation matrix (all scenarios/ES)
- `calculate_instrument_depreciations_light(n_instruments=100)` - ⚡ Lightweight depreciation
- `calculate_financial_impacts(depreciation_df)` - Calculate PD, LGD, price changes
- `calculate_shs_losses(financial_impacts)` - Aggregate portfolio losses by holder
- `run_full_pipeline(create_plots=True)` - Run complete SHS workflow
- `run_quick_test(n_instruments=100)` - ⚡ Quick test with limited data

**Output:** Portfolio losses aggregated by holder, sector, geography, ecosystem service, scenario

#### `AnaCreditAnalysisPipeline`

```python
from nature_analysis import AnaCreditAnalysisPipeline

pipeline = AnaCreditAnalysisPipeline()
```

**Methods:**
- `load_all_data()` - Load AnaCredit instruments, vulnerability, alpha, NACE mapping
- `calculate_instrument_depreciations()` - Calculate depreciation matrix (all scenarios/ES)
- `calculate_financial_impacts(depreciation_df)` - Calculate PD, LGD, price changes
- `run_full_pipeline()` - Run complete AnaCredit workflow

**Output:** Financial impacts by instrument (no holder aggregation)

### Convenience Functions

```python
import nature_analysis

# SHS analysis
shs_results = nature_analysis.run_pipeline(create_plots=True)
shs_quick = nature_analysis.run_quick_test(n_instruments=100)

# AnaCredit analysis
anacredit_results = nature_analysis.run_anacredit_pipeline()
anacredit_quick = nature_analysis.run_anacredit_quick_test(n_instruments=100)
```

**Functions:**
- `run_pipeline(create_plots=True)` - Run full SHS analysis pipeline
- `run_quick_test(n_instruments=100)` - ⚡ Run SHS quick test
- `run_anacredit_pipeline()` - Run full AnaCredit analysis pipeline
- `run_anacredit_quick_test(n_instruments=100)` - ⚡ Run AnaCredit quick test

### Data Loader Functions

```python
from nature_analysis import data_loader

# Load instrument data
shs_df = data_loader.load_SHS_data()
anacredit_df = data_loader.load_Anacredit_data()

# Load shared data
vuln_df = data_loader.load_vulnerability_data()
alpha_df = data_loader.load_alpha_data()
nace_map = data_loader.load_nace_mapping()
prod_df = data_loader.load_production_data()

# Load SHS-specific data
holder_df = data_loader.load_shs_holder_data()
```

### Vulnerability Calculation Functions

```python
from nature_analysis import vulnerability

# SHS depreciation
shs_depr = vulnerability.calculate_depreciation(
    instrument_df, vuln_df, alpha_df, nace_map, prod_df,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC'
)

# AnaCredit depreciation (wrapper around same logic)
anacredit_depr = vulnerability.calculate_anacredit_depreciation(
    instrument_df, vuln_df, alpha_df, nace_map, prod_df,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC'
)
```

---

## ✅ Testing

### Quick Installation Test

```bash
# Run quick test to verify installation (fastest)
python -c "import nature_analysis; nature_analysis.run_quick_test(n_instruments=10)"
```

### Comprehensive Testing

```bash
# Run full test suite
python tests/test_suite.py

# Quick validation
python tests/quick_compare.py

# Test import
python tests/test_import.py

# Run quick test examples
python examples/quick_test.py

# Run SHS examples
python examples/basic_usage.py

# Run AnaCredit examples
python examples/anacredit_usage.py
```

---

## 🔧 Troubleshooting

### Cannot import package

```bash
pip install -e .
```

### Missing data files

Update file paths in `nature_analysis/config.py` to point to your data location.

**For SHS analysis:**
- Update `SHS_INSTRUMENT_FILE`
- Update `SHS_HOLDER_FILE`

**For AnaCredit analysis:**
- Update `ANACREDIT_INSTRUMENT_FILE`

**For both:**
- Update `VULN_FILE`, `ALPHA_FILE`, `NACE_MAPPING_FILE`, etc.

### ImportError: No module named 'nature_analysis'

Make sure you've installed the package:
```bash
pip install -e .
```

### Different results between SHS and AnaCredit

This is expected! The pipelines use different data sources:
- **SHS**: Securities holdings → Portfolio aggregation by holder
- **AnaCredit**: Bank lending → Direct instrument-level impacts

The underlying calculation logic is identical, but the data and final aggregation differ.

---

## 📄 License

MIT License

---

## 👥 Contributors

- Original: Jupyter notebook by Seb
- v2.0: Modular Python package architecture with dual data source support
- Models: Merton structural credit risk framework

---

**Last Updated:** 2025-11-18
**Version:** 2.0.0
