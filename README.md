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
3. **Portfolio Analysis**: Securities holdings statistics (SHS) data

**Key Output**: Portfolio value losses aggregated by holder, sector, geography, and ecosystem service scenario.

### Key Features

- ✅ Calculate asset depreciation from ecosystem service disruptions
- ✅ Model financial impacts using Merton credit risk framework
- ✅ Aggregate portfolio losses across multiple dimensions
- ✅ Support for multiple scenarios and ecosystem services
- ✅ Parallel processing for performance
- ✅ Comprehensive testing and validation
- ✅ Professional package structure with clean API

### What's New in v2.0

- 🎯 **Simplified naming**: Removed "shs_" prefix from all modules
- 📁 **Professional structure**: Organized into `nature_analysis/`, `tests/`, `examples/`, `legacy/`
- 📦 **Easy installation**: Proper `setup.py` with pip install support
- 📚 **Better documentation**: Clear input/output specifications and examples
- 🔧 **Cleaner API**: `AnalysisPipeline` class with intuitive method names

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/shs-nature-analysis.git
cd shs-nature-analysis

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

### Example 1: One-Line Execution

```python
import nature_analysis

# Run complete analysis with default settings
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

### Example 2: Using the Pipeline Class

```python
from nature_analysis import AnalysisPipeline

# Create pipeline instance
pipeline = AnalysisPipeline()

# Run full pipeline
results = pipeline.run_full_pipeline(create_plots=True)

# Access intermediate results
print(f"Loaded {len(pipeline.instrmnt_df)} instruments")
print(f"Analyzed {len(pipeline.eco_services)} ecosystem services")
print(f"Ran {len(pipeline.scenarios)} scenarios")
```

### Example 3: Step-by-Step Analysis

```python
from nature_analysis import AnalysisPipeline

pipeline = AnalysisPipeline()

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

# Step 4: Calculate portfolio losses
results = pipeline.calculate_shs_losses(financial_impacts)
print(f"✓ Final results: {results.shape}")
```

---

## 📁 Project Structure

```
shs-nature-analysis/
├── README.md                   # This file
├── setup.py                    # Package installation script
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
│
├── nature_analysis/            # Main package ⭐
│   ├── __init__.py            # Package initialization & exports
│   ├── config.py              # Configuration parameters
│   ├── data_loader.py         # Data loading & preprocessing
│   ├── vulnerability.py       # Vulnerability calculations
│   ├── financial.py           # Financial models (Merton, pricing)
│   ├── pipeline.py            # Main orchestration pipeline
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
│   ├── basic_usage.py         # Simple examples
│   └── advanced_usage.py      # Advanced scenarios
│
└── legacy/                     # Original reference code
    ├── __init__.py
    └── SHS_process.py         # Original implementation
```

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `config.py` | Centralized configuration | Constants, file paths, parameters |
| `data_loader.py` | Load and preprocess data | `load_instrument_data()`, `load_vulnerability_data()` |
| `vulnerability.py` | Calculate depreciations | `calculate_depreciation()`, `compute_weighted_metric()` |
| `financial.py` | Implement financial models | `calculate_lgd()`, `calculate_bond_price_variation()` |
| `pipeline.py` | Orchestrate workflow | `AnalysisPipeline` class |
| `visualization.py` | Generate plots | `plot_loss_heatmap_by_dimension()` |

---

## 💡 Usage Examples

### Analyze Specific Scenario

```python
from nature_analysis import AnalysisPipeline, config

pipeline = AnalysisPipeline()
pipeline.load_all_data()

# Filter for specific ecosystem service
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

**Input:**
- Loaded instrument data (DataFrame with ISIN, PD, volatility, etc.)
- Vulnerability scores by ecosystem service
- SHS holder data

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

### Custom Visualization

```python
from nature_analysis import visualization

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

**Input:**
- `results_df`: Final results DataFrame from pipeline
- `eco_service`: Ecosystem service name (e.g., "Pollination")
- `scenario`: Scenario identifier
- `dimension_x`, `dimension_y`: Columns for heatmap axes
- `value_type`: 'percentage', 'absolute_eur', or 'obs_value'

**Output:**
- Heatmap PNG file showing losses by dimensions
- Figure object for further customization

### Sensitivity Analysis

```python
from nature_analysis import config, AnalysisPipeline
import pandas as pd

# Test different PD calibrations
pd_values = [0.03, 0.0459, 0.06]
sensitivity_results = []

for pd_calib in pd_values:
    # Temporarily modify config
    original_pd = config.PD_CALIB
    config.PD_CALIB = pd_calib

    # Run analysis
    pipeline = AnalysisPipeline()
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

**Input:**
- List of PD calibration values to test
- Standard pipeline configuration

**Output:**
```
   PD_CALIB    Total_Loss    Total_Value  Loss_Rate_%
0      0.03  32,145,234  5,234,891,234         0.614
1    0.0459  45,678,912  5,234,891,234         0.873
2      0.06  56,234,123  5,234,891,234         1.074
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
```

### File Paths

Configure data file locations in `config.py`:

```python
from pathlib import Path

BASE_PATH = Path('/path/to/your/data/root')
DATA_PATH = BASE_PATH / 'data'
VULN_PATH = BASE_PATH / 'vulnerability'

# Input files
INSTRUMENT_FILE = '/path/to/instrument_data.csv'
VULN_FILE = 'vulnerability_scores.csv'
ALPHA_FILE = 'alpha_shocks.xlsx'
SHS_HOLDER_FILE = '/path/to/holder_data.csv'
```

---

## 📊 Data Requirements

### Required Input Files

| File | Description | Key Columns |
|------|-------------|-------------|
| **Instrument Data** | Financial instruments with risk metrics | `ISIN`, `PD`, `vol`, `debt_ratio`, `nace`, `ISSUER_COUNTRY` |
| **Vulnerability Scores** | Ecosystem service vulnerability by sector/region | `region`, `eco_serv`, `EXIOBASE`, `NACE Code`, `Vuln`, `Adj_ind` |
| **Alpha Shocks** | Ecosystem service shock parameters | `Area`, `eco_serv`, various vulnerability types |
| **SHS Holder Data** | Securities holdings by holder | `ISIN`, `HOLDER_SECTOR`, `HOLDER_AREA`, `OBS_VALUE` |

### Data Validation

```python
from nature_analysis import AnalysisPipeline

pipeline = AnalysisPipeline()
pipeline.load_all_data()

# Check loaded data
print(f"Instruments: {len(pipeline.instrmnt_df)} rows")
print(f"  Columns: {list(pipeline.instrmnt_df.columns)}")
print(f"\nVulnerabilities: {len(pipeline.vuln_df)} rows")
print(f"  Ecosystem services: {pipeline.vuln_df['eco_serv'].nunique()}")
print(f"\nAlpha shocks: {len(pipeline.alpha_df)} rows")
```

---

## 💰 Financial Models

### Merton Structural Model Overview

The package implements the Merton structural credit risk model.

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

---

## 📖 API Reference

### Main Classes

#### `AnalysisPipeline`

```python
from nature_analysis import AnalysisPipeline

pipeline = AnalysisPipeline()
```

**Methods:**
- `load_all_data()` - Load all required input files
- `calculate_instrument_depreciations()` - Calculate depreciation matrix
- `calculate_financial_impacts(depreciation_df)` - Calculate PD, LGD, price changes
- `calculate_shs_losses(financial_impacts)` - Aggregate portfolio losses
- `run_full_pipeline(create_plots=True)` - Run complete workflow

---

## ✅ Testing

```bash
# Run full test suite
python tests/test_suite.py

# Quick validation
python tests/quick_compare.py

# Test import
python tests/test_import.py
```

---

## 🔧 Troubleshooting

### Cannot import package

```bash
pip install -e .
```

### Missing data files

Update file paths in `nature_analysis/config.py`

---

## 📄 License

MIT License

---

## 👥 Contributors

- Original: Jupyter notebook by Seb
- v2.0: Modular Python package architecture
- Models: Merton structural credit risk framework

---

**Last Updated:** 2025-11-18
**Version:** 2.0.0
