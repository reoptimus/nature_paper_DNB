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
- 📦 **Easy installation**: Standard `pyproject.toml` with pip install support
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

# With optional extras (see pyproject.toml [project.optional-dependencies]):
pip install -e ".[dev]"                      # ruff, bandit, mypy, pytest-cov
pip install -e ".[vulnerability-generation]"  # scikit-learn, tqdm
pip install -e ".[azure]"                     # DNB-internal only
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

### Dependencies

**Core** (enough for the financial models, vulnerability calculations, and
the shipped local reference/vulnerability data):
- **pandas** (>=1.3.0) - Data manipulation
- **numpy** (>=1.20.0) - Numerical computing
- **scipy** (>=1.7.0) - Scientific computing
- **matplotlib** (>=3.4.0) - Plotting
- **seaborn** (>=0.11.0) - Statistical visualizations
- **joblib** (>=1.0.0) - Parallel processing
- **openpyxl** (>=3.0.0) - Excel file support

**Optional, DNB-internal only** (needed only to load confidential SHS /
AnaCredit / COREP / ARS data from Azure - see [Data Sources: SHS vs AnaCredit](#data-sources-shs-vs-anacredit)):
- **azure-identity**, **azure-storage-file-datalake**, **azure-core**

**Optional, vulnerability regeneration only** (see
[Vulnerability Data Generation](#-vulnerability-data-generation-optional)):
- **scikit-learn** - PCA/clustering of ecosystem services
- **tqdm** - progress bars

`pip install -r requirements.txt` installs all of the above; the azure-\*
packages are imported lazily, so the core package works fine without them
if you only need the local/reference-data functionality.

---

## 🚀 Quick Start

### Example 0a: Demo Mode (No DNB Access Needed) 🎓

**The easiest way to see the whole pipeline work, right after cloning the
repo - no Azure, no credentials, no confidential data.**

```python
import nature_analysis

# Runs the full SHS pipeline (depreciation -> Merton model -> portfolio
# losses by holder) on a small synthetic instrument/holder dataset, using
# the real, non-confidential vulnerability data shipped in the repo.
results = nature_analysis.run_demo()

print(f"Total (fictitious) loss: €{results['VALUE_LOSS'].sum():,.0f}")
print(f"Average loss % by sector:")
print(results.groupby('nace_lvl1')['loss_perc'].mean().sort_values())
```

**Output** (actual run - agriculture (`A`) shows the largest average loss
%, as expected for a package quantifying nature dependency):
```
nace_lvl1
A   -0.172655
J   -0.115866
P   -0.110535
M   -0.103173
B   -0.086179
K   -0.050764
C   -0.049520
H   -0.049479
G   -0.037018
Name: loss_perc, dtype: float64
```

The instruments/holders are entirely fictitious (see
`examples/generate_demo_data.py` - regenerate with
`python examples/generate_demo_data.py`), but they are matched to real
country and NACE sector codes so the results reflect genuine
ecosystem-vulnerability patterns. Pass `n_instruments=` for an even faster
run, e.g. `nature_analysis.run_demo(n_instruments=30)`.

**Prefer a guided, cell-by-cell walkthrough?** Open
[`examples/demo_walkthrough.ipynb`](examples/demo_walkthrough.ipynb) in
Jupyter (`pip install jupyter`, then `jupyter notebook
examples/demo_walkthrough.ipynb`) - it runs the same demo with explanations
of the Merton model and two charts (loss by sector, loss by ecosystem
service).

### Example 0b: Quick Test on Real Data (Fast & Lightweight) ⚡

**Perfect for testing, demos, or first-time users - inside the DNB
environment.** `run_quick_test()` loads real SHS instrument data through
Azure, so it requires DNB Azure access; use Example 0a above if you don't
have that.

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

# Step 2: Calculate depreciation + financial impacts + portfolio losses
# (one call: it internally computes the depreciation matrix, applies the
# Merton model, and aggregates losses by holder)
results = pipeline.calculate_financial_impacts()
print(f"✓ Final results: {results.shape}")
```

`run_full_pipeline()` (used by `nature_analysis.run_pipeline()`) is just
`load_all_data()` followed by `calculate_financial_impacts()`.

---

## 📁 Project Structure

```
nature_paper_DNB/
├── README.md                   # This file
├── pyproject.toml              # Package metadata, dependencies, tool config (ruff/pytest/coverage)
├── requirements.txt            # Dependencies (pip install -r requirements.txt)
├── LICENSE                     # MIT
├── .gitignore                  # Git ignore rules
├── CLAUDE.md                   # Guide for AI assistants
├── .github/workflows/tests.yml # CI: lint + tests + coverage, no DNB access needed
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
│   ├── test_suite.py                    # Unit tests + optional output-diff tool
│   ├── test_import.py                   # Import / API surface validation
│   ├── test_vulnerability_generator.py  # pytest suite (mocked data, no DNB access needed)
│   ├── test_visualization.py            # pytest suite for visualization.py (mocked data)
│   └── quick_compare.py                 # Manual before/after CSV comparison (not auto-run)
│
├── examples/                   # Usage examples
│   ├── __init__.py
│   ├── demo_walkthrough.ipynb           # Notebook: run_demo() explained step by step, no DNB access needed
│   ├── generate_demo_data.py            # Regenerates data/demo/ (synthetic, no DNB access needed)
│   ├── basic_usage.py                   # SHS + AnaCredit + prudential workflows
│   ├── using_stored_vulnerabilities.py  # Standard workflow walkthrough
│   └── vulnerability_generation.py      # Regeneration workflow walkthrough
│
├── data/                       # Reference data (portable, no DNB access needed)
│   ├── demo/                             # Synthetic demo instruments/holders
│   ├── DS_Vuln_update/Vuln_final_store/  # Pre-generated Final_Vuln_file.csv / Final_alpha_file.xlsx
│   ├── EXIOBASE_to_NACElvl2_tab.xlsx     # NACE to EXIOBASE mapping
│   ├── regions_ISO2_continent_area.csv   # Region/country mapping
│   └── ...                               # Other reference files
│
└── legacy/                     # Original pre-refactor code (not maintained - see legacy/README.md)
    ├── __init__.py
    ├── README.md
    ├── SHS_process.py
    └── DS_functions.py
```

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `config.py` | Centralized configuration | Constants, file paths, parameters |
| `data_loader.py` | Load and preprocess data | `load_SHS_data()`, `load_Anacredit_data()`, `load_vulnerability_data()` |
| `vulnerability.py` | Calculate depreciations | `calculate_deltaPD_SHS()`, `calculate_deltaPD_anacredit()`, `compute_weighted_metric()` |
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
water_results = results[results['eco_service'] == 'Water flow regulation']

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

`plot_loss_heatmap_by_dimension()` is built for the *production-loss*
dataframe (columns `eco_serv`, `Vuln_type`, `delta_indout`, `indout`), not
directly for SHS/AnaCredit portfolio-loss results - use it with
`pipeline.prepare_production_loss_analysis()`:

```python
from nature_analysis import visualization, pipeline

data_prod_losses = pipeline.prepare_production_loss_analysis()

fig = visualization.plot_loss_heatmap_by_dimension(
    results_df=data_prod_losses,
    eco_service='Pollination',
    scenario='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',  # a value from data_prod_losses['Vuln_type']
    dimension_x='region',
    dimension_y='EXIOBASE',
    value_type='percentage',
    output_path='pollination_heatmap.png'
)

print("Visualization saved to pollination_heatmap.png")
```

To plot SHS/AnaCredit portfolio-loss results (`VALUE_LOSS`, `OBS_VALUE`,
`HOLDER_SECTOR`, ...) - e.g. the output of `run_demo()` or
`run_pipeline()` - use `plot_portfolio_loss_heatmap()` instead:

```python
from nature_analysis import visualization, SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(demo=True)  # or demo=False with DNB access

fig = visualization.plot_portfolio_loss_heatmap(
    results_df=results,
    eco_service=results['eco_service'].iloc[0],
    scenario=results['scenario'].iloc[0],
    dimension_x='HOLDER_SECTOR',
    dimension_y='nace_lvl1',
    value_type='percentage',
    output_path='portfolio_heatmap.png'
)

print("Visualization saved to portfolio_heatmap.png")
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
# SHS, AnaCredit and prudential workflow examples (each function is meant to
# be run interactively / cell-by-cell, not as a single top-to-bottom script)
python examples/basic_usage.py

# Standard workflow: using the pre-generated vulnerability files
python examples/using_stored_vulnerabilities.py

# Regeneration workflow: rebuilding Final_Vuln_file.csv / Final_alpha_file.xlsx
python examples/vulnerability_generation.py
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

`config.py` distinguishes two kinds of data, each with its own path convention:

**1. Local package data** (shipped in this repo's `data/` folder - portable,
no DNB access required):

```python
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / 'data'
VULN_PATH = DATA_PATH / 'DS_Vuln_update' / 'Vuln_final_store'  # Vuln/Alpha files
# NACE mapping, volatility, debt-ratio reference tables also live under DATA_PATH
```

These paths resolve automatically to the repository's own `data/` directory,
so `load_vulnerability_data()`, `load_alpha_data()` and `load_nace_mapping()`
work out of the box after cloning the repo - no DNB environment needed.

**2. Confidential DNB source data** (SHS, AnaCredit, COREP, ARS Solvency 2 -
Azure Data Lake only, DNB-internal):

```python
BASE_PATH = Path("./secure/Sebastien/Nature 3.0/Nature_analysis")  # Azure blob-path prefix, not a local path
account_name = "stfsifadsprd01"
container_name = "ctr-workbench"

SHS_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'SHS/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'
ANACREDIT_INSTRUMENT_FILE = SECURED_DRIVE_PATH / 'anacredit_NL/anacredit_df_2024-12-31.csv'
```

**Note:** Instrument-level data (SHS, AnaCredit, COREP, ARS) is confidential
DNB microdata and can only be loaded from inside the DNB secured Azure
environment - this is by design, not a configuration issue to work around.
Anyone outside DNB can still use the package for: the financial models
(`financial.py`), the vulnerability calculations against the shipped
reference/vulnerability files (`vulnerability.py`, `data_loader.load_vulnerability_data()`
etc.), and the vulnerability-generation workflow (with their own
ENCORE/EXIOBASE/ND-GAIN downloads).

---

## 🔄 Vulnerability Data Generation (Optional)

### 🌟 KEY FEATURE: One-Command Vulnerability Regeneration

**Generate vulnerability tables for ALL scenarios with a single function call:**

```python
import nature_analysis

# Automatically processes ALL scenario configs in data/DS_Vuln_update/config_store/
shapes = nature_analysis.regenerate_vulnerability_files()
```

**What it does:**
1. 🔍 **Automatically discovers** all `config_*.py` files in `data/DS_Vuln_update/config_store/`
2. 🔄 **Processes each scenario** (World 10%, EU 3%, custom scenarios, etc.)
3. 📊 **Generates vulnerability scores** from ENCORE + EXIOBASE + ND-GAIN data
4. 💾 **Outputs two files:**
   - `Final_Vuln_file.csv` - Vulnerability scores for all scenarios
   - `Final_alpha_file.xlsx` - Shock parameters for all scenarios

**No instrument data needed!** This workflow is completely independent of SHS/AnaCredit financial analysis.

---

### Two Workflows

The package supports two workflows for handling vulnerability data:

| Workflow | Description | Time | When to Use |
|----------|-------------|------|-------------|
| **Standard** (Recommended) | Use pre-generated `Final_Vuln_file.csv` and `Final_alpha_file.xlsx` | Minutes | Regular portfolio analysis |
| **Regeneration** (Key Feature) | Generate vulnerability files from ENCORE/EXIOBASE/ND-GAIN | 10-30 min | Updating underlying vulnerability data |

### 💡 Why This Is Powerful

Vulnerability generation is **completely independent** of financial analysis. You can:
- ✅ **No instrument data required** - Generate vulnerability tables without any SHS or AnaCredit data
- ✅ **Automatic scenario discovery** - Just add `config_*.py` files, function finds them all
- ✅ **Test multiple scenarios** - 5%, 10%, 15% shocks, different rating mappings, regional variations
- ✅ **Update data independently** - New ENCORE/EXIOBASE releases without re-processing portfolios
- ✅ **Rapid scenario testing** - Add new scenario config (62 lines), regenerate in 10-30 min

**Key Insight:** Vulnerability scores are **scenario-specific** but **instrument-agnostic** – they describe sector-country-ecosystem relationships, not individual securities. Generate once, use with any instrument dataset.

### Standard Workflow: Using Pre-Generated Files

**This is the recommended approach** for regular analysis:

```python
import nature_analysis

# Use pre-generated vulnerability files (stored in data directory)
results = nature_analysis.run_pipeline()

# Or for AnaCredit
results = nature_analysis.run_anacredit_pipeline()
```

The vulnerability files (`Final_Vuln_file.csv` and `Final_alpha_file.xlsx`) contain sector-level vulnerability scores that are **scenario-specific** but **instrument-agnostic**. They can be reused across different instrument datasets (SHS or AnaCredit).

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

#### 🎯 Method 1: One Function Call (Recommended)

**The simplest way - automatically processes all scenarios:**

```python
import nature_analysis

# That's it! Automatically discovers and processes ALL config files
shapes = nature_analysis.regenerate_vulnerability_files()

print(f"Generated Alpha file: {shapes['alpha']}")  # (rows, cols)
print(f"Generated Vuln file: {shapes['vuln']}")    # (rows, cols)
```

**What happens automatically:**
- ✅ Discovers all `config_*.py` files in `data/DS_Vuln_update/config_store/`
- ✅ For each config: Loads ENCORE → Builds Leontief matrix → Calculates DS/Vuln → Generates Alpha
- ✅ Merges all scenarios into `Final_Vuln_file.csv` and `Final_alpha_file.xlsx`
- ✅ Returns file shapes for verification

**Time:** 10-30 minutes depending on number of scenarios (e.g., 4 scenarios ≈ 15-20 min)

#### Method 2: Interactive Example Script

```bash
python examples/vulnerability_generation.py
```

Provides step-by-step guidance, configuration validation, and progress indicators.

#### Method 3: See Usage Examples

```bash
# Show how to use stored vulnerability files
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
Final_Vuln_file.csv + Final_alpha_file.xlsx
```

**Output Files:**
- `Final_Vuln_file.csv` - Vulnerability scores per region/sector/ecosystem service/scenario
- `Final_alpha_file.xlsx` - Shock parameters per area/ecosystem service/scenario

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

# 5. Price Impact (bonds)
variation = financial.calculate_bond_price_variation(
    duration=5.0, pd=0.05, lgd=0.65, delta_pd=0.01, delta_lgd=0.0
)

# 6. Price Impact (equity, Merton model)
equity_variation = financial.calculate_equity_price_variation(
    pd=0.05, delta_pd=0.01, sigma=0.25
)
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
- `load_all_data(demo=False)` - Load SHS instruments, vulnerability, alpha, NACE mapping, holder data. `demo=True` loads the synthetic dataset (`data/demo/`) instead of confidential SHS data - no Azure access needed.
- `calculate_financial_impacts()` - Calculate depreciation, PD/LGD/price changes, and aggregate portfolio losses by holder (one call - no separate depreciation/aggregation steps)
- `run_full_pipeline(create_plots=False, demo=False)` - `load_all_data(demo=...)` + `calculate_financial_impacts()`
- `run_quick_test(n_instruments=100, demo=False)` - ⚡ Same, but limited to `n_instruments` instruments, the first scenario, and the first ecosystem service

**Output:** Portfolio losses aggregated by holder, sector, geography, ecosystem service, scenario

**Note:** `create_plots=True` saves one portfolio-loss heatmap (holder
sector x issuer sector, for the first scenario/ecosystem service in the
results) via `visualization.create_visualizations()` /
`plot_portfolio_loss_heatmap()`, to `config.ANALYSIS_PATH`. For other
dimensions/scenarios, call `visualization.plot_portfolio_loss_heatmap()`
directly (see [Custom Visualization](#custom-visualization)). Note that
`plot_loss_heatmap_by_dimension()` and `plot_loss_heatmap_by_region()` are
a different pair of functions, built for the *production-loss* dataframe
returned by `pipeline.prepare_production_loss_analysis()` (columns
`eco_serv`, `Vuln_type`, `delta_indout`, `indout`), not for SHS
portfolio-loss results.

#### `AnaCreditAnalysisPipeline`

```python
from nature_analysis import AnaCreditAnalysisPipeline

pipeline = AnaCreditAnalysisPipeline()
```

**Methods:**
- `load_all_data()` - Load AnaCredit instruments, vulnerability, alpha, NACE mapping
- `calculate_delta_CET1()` - Calculate PD/EL/RWA variation per credit line, merge with COREP, and return delta CET1 ratio per institution (requires DNB Azure access for AnaCredit + COREP data)
- `run_full_pipeline()` - `load_all_data()` + `calculate_delta_CET1()`
- `run_quick_test(n_instruments=100)` - ⚡ Same, limited to `n_instruments` instruments/first scenario/first ES (still requires COREP access - only compute time is reduced)

**Output:** Delta CET1 ratio per institution, scenario, ecosystem service

### Convenience Functions

```python
import nature_analysis

# No DNB access needed
demo_results = nature_analysis.run_demo()

# SHS analysis (requires DNB Azure access)
shs_results = nature_analysis.run_pipeline(create_plots=True)
shs_quick = nature_analysis.run_quick_test(n_instruments=100)

# AnaCredit analysis (requires DNB Azure access)
anacredit_results = nature_analysis.run_anacredit_pipeline()
anacredit_quick = nature_analysis.run_anacredit_quick_test(n_instruments=100)
```

**Functions:**
- `run_demo(n_instruments=None)` - 🎓 Run the full SHS pipeline on the synthetic demo dataset - no DNB access needed
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

# SHS: PD variation for one scenario/ecosystem service (used internally by
# SHSAnalysisPipeline.calculate_financial_impacts())
shs_delta_pd = vulnerability.calculate_deltaPD_SHS(
    vuln_df, instrument_df, alpha_df,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    option=config.AGGREG_TYPE,
    nace_map=nace_map,
    dep_type=config.DEPENDENCY_TYPE
)

# All scenarios/ES in parallel
all_shs_delta_pd = vulnerability.calculate_all_deltaPD_SHS(
    vuln_df, instrument_df, alpha_df, eco_services, scenarios,
    nace_map, config.AGGREG_TYPE, config.DEPENDENCY_TYPE
)

# AnaCredit: same idea, plus EL/RWA/CET1 variation (see AnaCreditAnalysisPipeline.calculate_delta_CET1())
anacredit_delta_pd = vulnerability.calculate_deltaPD_anacredit(
    vuln_df, instrument_df, alpha_df,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    option=config.AGGREG_TYPE,
    nace_map=nace_map,
    dep_type=config.DEPENDENCY_TYPE
)
```

---

## ✅ Testing

### What can run without DNB access

These checks require no confidential data and no Azure credentials - they
work right after `pip install -e .` on any machine:

```bash
pip install -e ".[dev,vulnerability-generation]"

# 1. Import + public API surface check
python tests/test_import.py

# 2. Unit tests for the Merton/financial formulas and vulnerability helpers,
#    plus an end-to-end run of the SHS pipeline on the synthetic demo
#    dataset (see Example 0a) - the one integration test that can run
#    anywhere. Also includes an optional before/after CSV diff tool that
#    just reports "skipped" when no comparison files are present.
python tests/test_suite.py

# 3. pytest suite for the vulnerability-generation module (uses mocked data)
# and 4. pytest suite for visualization.py (heatmaps, summary stats)
python -m pytest tests/test_vulnerability_generator.py tests/test_visualization.py -v

# Lint + coverage (same checks as CI, see .github/workflows/tests.yml)
python -m ruff check nature_analysis/
python -m pytest --cov=nature_analysis --cov-report=term-missing tests/
```

### What requires DNB Azure access

`nature_analysis.run_quick_test()` / `run_pipeline()` and the AnaCredit
equivalents load real SHS/AnaCredit/COREP instrument data through Azure -
they only work from inside the DNB secured environment:

```bash
python -c "import nature_analysis; nature_analysis.run_quick_test(n_instruments=10)"
python examples/basic_usage.py
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

[MIT License](LICENSE) - see the `LICENSE` file. The copyright holder
listed there (`Nature Analysis Team`) is a placeholder matching
`pyproject.toml`'s `authors` field; update it to the appropriate legal
entity before distributing the package externally.

---

## 👥 Contributors

- Original: Jupyter notebook by Seb
- v2.0: Modular Python package architecture with dual data source support
- Models: Merton structural credit risk framework

---

**Last Updated:** 2025-11-18
**Version:** 2.0.0
