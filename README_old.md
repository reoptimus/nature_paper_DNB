# SHS Nature Analysis

> **Securities Holdings Statistics (SHS) Nature-Based Financial Risk Analysis**
>
> A production-ready Python package for quantifying how ecosystem service disruptions impact financial portfolios through credit risk modeling.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Data Requirements](#data-requirements)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Financial Models](#financial-models)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [For AI Assistants](#for-ai-assistants)
- [Contributing](#contributing)

---

## Overview

### What This Project Does

This system quantifies how disruptions to **ecosystem services** (e.g., water regulation, pollination, soil retention) propagate through the economy to affect **financial portfolios**. It combines:

1. **Ecosystem Science**: Vulnerability of economic sectors to nature degradation
2. **Financial Theory**: Merton structural model for credit risk
3. **Portfolio Analysis**: Securities holdings statistics (SHS) data

**Key Output**: Portfolio value losses by holder, sector, geography, and ecosystem service scenario.

### Key Capabilities

- ✓ Calculate asset depreciation from ecosystem service disruptions
- ✓ Model financial impacts using Merton credit risk framework
- ✓ Aggregate portfolio losses across multiple dimensions
- ✓ Support multiple scenarios and ecosystem services
- ✓ Parallel processing for performance
- ✓ Comprehensive testing and validation

### Project History

- **Origin**: Jupyter notebook (`shs_nature_analysis_Seb.ipynb`)
- **Refactoring**: Transformed into modular Python package
- **Status**: Production-ready with comprehensive testing

---

## Quick Start

### Option 1: As a Package (Recommended)

```python
import shs_nature_analysis as shs

# Run complete analysis with one function
results = shs.run_pipeline(create_plots=True)
print(f"Analysis complete! Results shape: {results.shape}")
```

### Option 2: Using the Pipeline Class

```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

### Option 3: Step-by-Step Execution

```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()

# Load data
pipeline.load_all_data()
print(f"Loaded {len(pipeline.instrument_df)} instruments")

# Calculate depreciations
depreciation_df = pipeline.calculate_instrument_depreciations()

# Calculate financial impacts
financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)

# Calculate portfolio losses
final_results = pipeline.calculate_shs_losses(financial_impacts)
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
```

### Package Setup

**Important**: The directory name uses hyphens (`shs-nature-analysis`) but Python requires underscores. Choose one solution:

**Option A: Rename the directory (recommended)**
```bash
cd /path/to/parent
mv shs-nature-analysis shs_nature_analysis
```

**Option B: Create a symbolic link**
```bash
cd /path/to/parent
ln -s shs-nature-analysis shs_nature_analysis
```

**Option C: Install as editable package** (requires `setup.py`)
```bash
cd shs-nature-analysis
pip install -e .
```

### Using the Package

Once installed, you can import from anywhere:

```python
import sys
sys.path.insert(0, '/path/to/parent/directory')

import shs_nature_analysis as shs
results = shs.run_pipeline()
```

---

## Project Structure

```
shs-nature-analysis/
├── __init__.py                # 📦 Package initialization & exports
├── shs_config.py              # ⚙️  Configuration (parameters, paths)
├── shs_data_loader.py         # 📊 Data loading and preprocessing
├── shs_vulnerability.py       # 🔢 Vulnerability & depreciation calculations
├── shs_financial.py           # 💰 Financial models (Merton, pricing)
├── shs_main_pipeline.py       # 🚀 Main orchestration pipeline
├── shs_visualization.py       # 📈 Plotting and visualization
├── shs_test_suite.py          # ✅ Comprehensive test suite
├── shs_example_usage.py       # 📚 Six usage examples
├── shs_quick_compare.py       # 🔍 Fast output validation
├── SHS_process.py             # 📜 Original code (reference only)
├── README.md                  # 📖 This file
└── data/                      # 📁 Input data files
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `shs_config.py` | Centralized configuration for all parameters |
| `shs_data_loader.py` | Load and preprocess all input data |
| `shs_vulnerability.py` | Calculate weighted vulnerabilities and depreciations |
| `shs_financial.py` | Implement Merton model and pricing functions |
| `shs_main_pipeline.py` | Orchestrate the complete workflow |
| `shs_visualization.py` | Generate heatmaps and charts |
| `shs_test_suite.py` | Validate against original implementation |

### Data Flow

```
Raw Data Files
    ↓
[Data Loader] → Load & preprocess
    ↓
Instrument + Vulnerability + Alpha Shocks
    ↓
[Vulnerability Calculator] → Parallel depreciation calculations
    ↓
Depreciation Matrix (instruments × scenarios)
    ↓
[Financial Models] → Calculate price variations (Merton)
    ↓
Financial Impacts DataFrame
    ↓
[Pipeline Aggregation] → Merge with holder data
    ↓
Final Results CSV + Visualizations
```

---

## Data Requirements

### Required Data Files

The analysis requires the following data files to be available. File paths are configured in `shs_config.py`.

#### 1. Core Input Files

| File | Description | Format | Expected Location |
|------|-------------|--------|-------------------|
| **Instrument Data** | Financial instruments with ISIN, PD, volatility, debt ratio, NACE code | CSV | `INSTRUMENT_FILE` in config |
| **Vulnerability Scores** | Ecosystem service vulnerability by region, EXIOBASE sector, and NACE code | CSV | `VULN_PATH/VULN_FILE` |
| **Alpha Shocks** | Ecosystem service shock parameters by area and vulnerability type | Excel (.xlsx) | `VULN_PATH/ALPHA_FILE` |
| **SHS Holder Data** | Securities holdings statistics linking holders to instruments | CSV | `SHS_HOLDER_FILE` in config |

#### 2. Mapping and Reference Files

| File | Description | Format | Expected Location |
|------|-------------|--------|-------------------|
| **EXIOBASE Production Data** | Industry output data (X matrix) for production weighting | CSV | `X_FILE` in config |
| **NACE Mapping** | Simple NACE code mapping table | Excel (.xlsx) | `DATA_PATH/nace_0d_map.xlsx` |
| **EXIOBASE to NACE Mapping** | Links EXIOBASE sectors to NACE Level 2 codes | Excel (.xlsx) | `DATA_PATH/EXIOBASE_to_NACElvl2_tab.xlsx` |
| **Region/Area Mapping** | ISO2 country codes to continent/area mapping | CSV | `./data/regions_ISO2_continent_area.csv` |

#### 3. Data Directory Structure

Create the following directory structure:

```
shs-nature-analysis/
├── data/
│   ├── regions_ISO2_continent_area.csv      # Region mapping (local)
│   ├── nace_0d_map.xlsx                     # NACE mapping (if using local)
│   └── EXIOBASE_to_NACElvl2_tab.xlsx        # EXIOBASE mapping (if using local)
└── [External paths configured in shs_config.py]
```

#### 4. Expected Data Schemas

**Instrument Data (`INSTRUMENT_FILE`):**
- Required columns: `ISIN`, `PD`, `vol` (volatility), `debt_ratio`, `nace`, `INSTR_CLASS`, `resid_mat_yr`, `ISSUER_COUNTRY`
- Data types: `nace` should be string type

**Vulnerability Data (`VULN_FILE`):**
- Required columns: `region`, `eco_serv`, `EXIOBASE`, `indout`, `NACE Code`, `Adj_ind`
- Additional columns: Various vulnerability type columns (e.g., `DS_total_SR`, `Vuln_total_SR`)

**Alpha Data (`ALPHA_FILE`):**
- Required columns: `Area`, `eco_serv`
- Additional columns: Various vulnerability type columns matching those in vulnerability data

**SHS Holder Data (`SHS_HOLDER_FILE`):**
- Required columns: `ISIN`, `HOLDER_SECTOR`, `HOLDER_AREA`, `VALUE`

**Region Mapping (`regions_ISO2_continent_area.csv`):**
- Required columns: `area`, `region` (ISO2 country code)

#### 5. Configuration

Before running the analysis, update file paths in `shs_config.py`:

```python
# Example configuration (shs_config.py)
BASE_PATH = Path('/path/to/your/data/root')
DATA_PATH = BASE_PATH / 'git_repo/Ecosystem_ds/data'
VULN_PATH = BASE_PATH / 'DS_Vuln_update/Vuln_final_store'

INSTRUMENT_FILE = '/path/to/F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv'
VULN_FILE = 'Vuln_final_03_11_2025.csv'
ALPHA_FILE = 'Alpha_final_03_11_2025.xlsx'
SHS_HOLDER_FILE = '/path/to/F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv'
```

#### 6. Data Validation

To verify your data files are correctly loaded:

```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
pipeline.load_all_data()

# Check what was loaded
print(f"Instruments: {len(pipeline.instrument_df)} rows")
print(f"Vulnerabilities: {len(pipeline.vulnerability_df)} rows")
print(f"Alpha shocks: {len(pipeline.alpha_df)} rows")
print(f"Holders: {len(pipeline.holder_df)} rows")
```

---

## Usage Guide

### Exported Components

The package exports:

- **`run_pipeline()`** - Convenience function for complete analysis
- **`SHSAnalysisPipeline`** - Main pipeline class
- **`config`** - Configuration module (alias for `shs_config`)
- **`data_loader`** - Data loading functions
- **`vulnerability`** - Vulnerability calculations
- **`financial`** - Financial modeling
- **`visualization`** - Plotting functions

### Common Tasks

#### Task 1: Run Full Analysis with Default Settings

```python
import shs_nature_analysis as shs

results = shs.run_pipeline(create_plots=True)

# Output files created:
# - merged_SHS_instr_vulnxalpha_scenarios_*.csv
# - shs_2024-Q4_results.csv
# - Various heatmap PNGs
```

#### Task 2: Analyze Specific Scenario

```python
from shs_nature_analysis import SHSAnalysisPipeline, vulnerability, config

pipeline = SHSAnalysisPipeline()
pipeline.load_all_data()

# Calculate depreciations for single ecosystem service
dep_df = vulnerability.calculate_depreciation(
    vuln_df=pipeline.vulnerability_df,
    instrmnt_df=pipeline.instrument_df,
    alpha_df=pipeline.alpha_df,
    nace_map_df=pipeline.nace_map_df,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    dep_type=config.DEPENDENCY_TYPE,
    aggreg_type=config.AGGREG_TYPE,
    nace_level=2
)
```

#### Task 3: Custom Visualization

```python
from shs_nature_analysis import visualization

fig = visualization.plot_loss_heatmap_by_dimension(
    results_df=results,
    eco_service='Pollination',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    dimension_x='HOLDER_SECTOR',
    dimension_y='HOLDER_AREA',
    value_type='percentage',
    figsize=(14, 10)
)
fig.savefig('custom_heatmap.png', dpi=300, bbox_inches='tight')
```

#### Task 4: Sensitivity Analysis

```python
from shs_nature_analysis import config, SHSAnalysisPipeline

# Test different PD calibrations
for pd_calib in [0.03, 0.0459, 0.06]:
    original_pd = config.PD_CALIB
    config.PD_CALIB = pd_calib

    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)
    results.to_csv(f'results_pd_{pd_calib}.csv', index=False)

    config.PD_CALIB = original_pd  # Restore
```

#### Task 5: Export Specific Results

```python
# Filter for specific criteria
filtered = results[
    (results['eco_service'] == 'Water flow regulation') &
    (results['HOLDER_AREA'] == 'NL')
]

# Export to Excel
filtered.to_excel('nl_water_results.xlsx', index=False)
```

### Six Complete Examples

See `shs_example_usage.py` for comprehensive examples:

1. **Example 1**: Full pipeline execution
2. **Example 2**: Custom scenario analysis
3. **Example 3**: Sensitivity analysis
4. **Example 4**: Country-specific analysis
5. **Example 5**: Custom visualizations
6. **Example 6**: Data export workflows

---

## Configuration

### Key Parameters

Edit `shs_config.py` to customize analysis:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RISK_FREE_RATE` | float | 0.02 | Annual risk-free interest rate |
| `CORRELATION_RHO` | float | 0.1 | Asset correlation |
| `PD_CALIB` | float | 0.0459 | Calibration probability of default |
| `LGD_CALIB` | float | 0.652 | Calibration loss given default |
| `MAX_MATURITY` | int | 30 | Maximum bond maturity (years) |
| `AGGREG_TYPE` | str | 'SR' | Aggregation type: 'SR' or 'max' |
| `DEPENDENCY_TYPE` | str | 'Vuln_total' | Dependency metric type |

### Example Configuration

```python
# In shs_config.py

# Financial parameters
RISK_FREE_RATE = 0.02          # 2% annual rate
CORRELATION_RHO = 0.1          # 10% correlation
PD_CALIB = 0.0459             # 4.59% calibration PD
LGD_CALIB = 0.652             # 65.2% loss rate

# Analysis settings
AGGREG_TYPE = 'SR'            # Sum of ratios
DEPENDENCY_TYPE = 'Vuln_total' # Use total vulnerability

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

---

## Financial Models

### Merton Structural Model

**Foundation**: Firm equity is modeled as a call option on firm assets.

#### Key Components

**1. Distance to Default (DD)**

Measures how far a firm is from default:

```
DD = -Φ⁻¹(PD)
```

where Φ is the cumulative standard normal distribution.

**2. Asset Volatility (σ_V)**

Derived from equity volatility using the Merton model:

```python
σ_V = (σ_equity / Φ(DD)) × (1 - debt_ratio)
```

**3. Loss Given Default (LGD)**

Incorporates correlation and calibration:

```python
lgd = lgd_calib × sqrt(
    (1 - ρ) × Φ(Φ⁻¹(PD) / sqrt(1-ρ)) / PD + ρ
)
```

**4. Risky Bond Pricing**

Credit-risky bond price with default risk:

```
B = 1 + (c - r - PD×LGD) × [1 - e^(-(r+PD)×T)] / (r + PD)
```

where:
- c = coupon rate
- r = risk-free rate
- T = maturity

**5. Equity Pricing**

Equity value as a call option (Merton):

```
E = V × Φ(d₁) - D × e^(-rT) × Φ(d₂)
```

### Ecosystem Depreciation Mechanism

**Flow**:
1. Ecosystem service disruption → Production decline
2. Production decline → Firm asset value falls
3. Asset depreciation reduces distance to default
4. Lower DD → Higher PD → Higher credit spread
5. Higher spread → Lower bond/equity prices
6. Price change × position = Portfolio loss

**Implementation**:
```python
# Calculate depreciation
depreciation = vulnerability × adjustment × alpha_shock

# Apply to distance to default
DD_new = DD_original - (depreciation / σ_V)

# Convert to new PD
PD_new = Φ(-DD_new)

# Calculate price variation
price_variation = calculate_price_change(PD_new, LGD_new, ...)
```

---

## Testing

### Running Tests

**Full test suite**:
```bash
python shs_test_suite.py
```

**Quick validation**:
```bash
python shs_quick_compare.py
```

**Specific test**:
```bash
python -c "from shs_test_suite import test_financial_functions; test_financial_functions()"
```

### Test Coverage

1. **Unit Tests**: Individual function validation
   - PD/DD conversions
   - Asset volatility calculations
   - LGD formulas
   - Bond/equity pricing

2. **Integration Tests**: End-to-end workflow
   - Compare refactored vs. original outputs
   - Validate pipeline consistency
   - Check output formats

3. **Validation Tests**: Numeric accuracy
   - 1% tolerance for floating-point comparisons
   - Shape and column consistency
   - Statistical summaries

### Adding New Tests

```python
# In shs_test_suite.py

def test_new_feature():
    """Test description."""
    # Arrange
    input_data = create_test_data()

    # Act
    result = new_function(input_data)

    # Assert
    expected = calculate_expected()
    assert np.allclose(result, expected, rtol=0.01)
    logger.info("✓ New feature test passed")

# Add to main():
test_new_feature()
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Missing Country in Alpha Data

**Symptom**: Warning "Country {X} not found in alpha data, using default (NL)"

**Solution**:
- Add country to alpha data file, OR
- Modify default in `shs_vulnerability.py`:
  ```python
  if pd.isna(country) or country not in country_list:
      country = 'US'  # Change default here
  ```

#### Issue 2: Low NACE Match Rate

**Symptom**: Many NaN values in depreciation output

**Solutions**:
- Check NACE mapping completeness
- Hierarchical matching tries levels 0, -1, -2 automatically
- Add more EXIOBASE sector mappings

#### Issue 3: Slow Performance

**Symptom**: Pipeline takes > 10 minutes

**Solutions**:

1. **Check parallel processing**:
   ```python
   # In shs_vulnerability.py
   n_jobs = -1  # Use all cores
   ```

2. **Filter data early**:
   ```python
   scenarios_to_run = ['Scenario_1', 'Scenario_2']
   alpha_df = alpha_df[alpha_df['scenario'].isin(scenarios_to_run)]
   ```

3. **Profile code**:
   ```python
   import cProfile
   cProfile.run('pipeline.run_full_pipeline()', 'profile_stats')
   ```

#### Issue 4: Memory Issues

**Symptom**: Out of memory errors

**Solutions**:

1. **Process in batches**:
   ```python
   for eco_service in config.ECO_SERVICES:
       results_subset = pipeline.run_full_pipeline(
           eco_services=[eco_service]
       )
       results_subset.to_csv(f'results_{eco_service}.csv')
   ```

2. **Optimize dtypes**:
   ```python
   df['HOLDER_SECTOR'] = df['HOLDER_SECTOR'].astype('category')
   df['eco_service'] = df['eco_service'].astype('category')
   ```

#### Issue 5: Test Failures

**Symptom**: Test suite reports differences > 1%

**Solutions**:
1. Check specific columns with failures
2. Inspect diff report for patterns
3. Adjust tolerance if differences are acceptable:
   ```python
   validator = OutputValidator(rtol=0.02)  # 2% tolerance
   ```

#### Issue 6: Missing Data Files

**Symptom**: `FileNotFoundError`

**Solutions**:
1. Check paths in `shs_config.py`
2. Use absolute paths:
   ```python
   INSTRUMENT_FILE = Path("/home/user/data/instruments.csv")
   ```

### Debugging Checklist

- [ ] Check log output for warnings/errors
- [ ] Verify input data files exist and have expected structure
- [ ] Inspect intermediate DataFrames after each stage
- [ ] Run quick comparison to identify failing stage
- [ ] Check for NaN/Inf values in critical columns
- [ ] Verify configuration parameters
- [ ] Ensure dependencies are installed (`pip list`)
- [ ] Check memory and disk space
- [ ] Review recent changes

---

## For AI Assistants

### When Working with This Codebase

**Priority Guidelines**:

1. **Always start with `shs_config.py`** to understand current parameters
2. **Use the pipeline class** rather than calling functions directly
3. **Validate changes** with test suite before considering them complete
4. **Preserve financial accuracy**: These are real-world risk calculations
5. **Document assumptions**: Financial modeling involves choices
6. **Consider performance**: Processes large datasets
7. **Maintain modularity**: Keep functions focused and testable
8. **Add logging**: Help users debug
9. **Update tests**: When modifying logic, update validation
10. **Update this file**: Keep documentation current

### Common Pitfalls to Avoid

- ❌ Don't break the Merton model (formulas are mathematically precise)
- ❌ Don't ignore NaN values (cascades through pipeline)
- ❌ Don't remove validation (prevents silent failures)
- ❌ Don't change config defaults without understanding implications
- ❌ Don't skip tests (regression testing is critical)
- ❌ Don't optimize prematurely (clarity > speed until bottleneck proven)

### Best Practices

- ✓ Read before writing (understand existing patterns)
- ✓ Test incrementally (run tests after each change)
- ✓ Log meaningfully (help future debuggers)
- ✓ Document domain knowledge (financial concepts are complex)
- ✓ Preserve provenance (keep links to original implementation)

### Function Reference

| Function | Module | Purpose |
|----------|--------|---------|
| `load_instrument_data()` | data_loader | Load financial instruments |
| `load_vulnerability_data()` | data_loader | Load ecosystem dependencies |
| `calculate_depreciation()` | vulnerability | Calculate asset depreciation |
| `compute_weighted_metric()` | vulnerability | Production-weighted averaging |
| `pd_to_dd()` | financial | Convert PD to distance to default |
| `calculate_asset_volatility()` | financial | Derive asset volatility |
| `calculate_lgd()` | financial | Calculate loss given default |
| `calculate_risky_bond_price()` | financial | Price credit-risky bonds |
| `calculate_bond_price_variation()` | financial | Bond price change from shock |
| `calculate_equity_price_variation()` | financial | Equity price change (Merton) |
| `plot_loss_heatmap_by_dimension()` | visualization | Flexible 2D heatmap |

### Making Changes

**Pattern**: Add function → Add tests → Document

```python
# 1. Add function to appropriate module
def new_pricing_model(param1: float, param2: float) -> float:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description

    Returns:
        Result description
    """
    # Implementation
    return result

# 2. Add unit test
def test_new_pricing_model():
    result = new_pricing_model(1.0, 2.0)
    assert abs(result - expected) < 1e-6

# 3. Update this README.md file
```

---

## Contributing

### Code Style

- **PEP 8 compliance**: Follow standard Python style
- **Line length**: 100 characters (not strict 79)
- **Indentation**: 4 spaces (no tabs)
- **Type hints**: Always include for parameters and returns

### Type Hints Example

```python
def calculate_metric(
    data: pd.DataFrame,
    weight_col: str,
    value_col: str,
    threshold: float = 0.5
) -> float:
    """Function docstring."""
    ...
```

### Docstring Format

Use Google style:

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

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Module | lowercase_with_underscores | `shs_data_loader.py` |
| Class | PascalCase | `SHSAnalysisPipeline` |
| Function | lowercase_with_underscores | `calculate_depreciation()` |
| Variable | lowercase_with_underscores | `instrument_df` |
| Constant | UPPER_SNAKE_CASE | `RISK_FREE_RATE` |
| Private | _leading_underscore | `_internal_helper()` |

### Error Handling Pattern

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

Use logging module, not print:

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed diagnostic information")
logger.info("General progress information")
logger.warning("Something unexpected but handled")
logger.error("Error that prevents operation")
```

### When Adding New Features

1. Keep functions focused and single-purpose
2. Add type hints to all signatures
3. Include docstrings with Args/Returns
4. Add logging at key steps
5. Write tests for new functionality
6. Update this README

---

## Output Files

The pipeline generates:

1. **Depreciation Matrix**:
   - File: `merged_SHS_instr_vulnxalpha_scenarios_{DEP_TYPE}_{AGGREG_TYPE}.csv`
   - Structure: Instruments × scenarios (wide format)
   - Values: Depreciation percentages

2. **Final Results**:
   - File: `shs_2024-Q4_results.csv`
   - Structure: Long format with all dimensions
   - Columns: ISIN, HOLDER_SECTOR, HOLDER_AREA, eco_service, scenario, VALUE, VALUE_LOSS

3. **Visualizations** (optional):
   - Heatmaps by NACE code and region
   - Loss distributions by dimension
   - Summary statistics charts

---

## Package Version

Current version: **1.0.0**

```python
import shs_nature_analysis as shs
print(shs.__version__)  # Output: 1.0.0
```

---

## License

[Your license here]

---

## Contact

[Your contact information]

---

## Acknowledgments

- Original implementation: Jupyter notebook by Seb
- Refactoring: Modular Python package architecture
- Financial models: Based on Merton structural credit risk framework
- Ecosystem data: EXIOBASE sector classifications

---

**Last Updated**: 2025-11-15
