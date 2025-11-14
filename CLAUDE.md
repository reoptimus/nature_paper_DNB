# CLAUDE.md - AI Assistant Guide for SHS Nature Analysis

> **Last Updated**: 2025-11-14
> **Project**: Securities Holdings Statistics (SHS) Nature-Based Financial Risk Analysis
> **Purpose**: Guide for AI assistants working with this codebase

---

## Table of Contents
- [Project Overview](#project-overview)
- [Quick Reference](#quick-reference)
- [Codebase Architecture](#codebase-architecture)
- [Module Guide](#module-guide)
- [Development Workflows](#development-workflows)
- [Common Tasks](#common-tasks)
- [Testing Strategy](#testing-strategy)
- [Coding Conventions](#coding-conventions)
- [Financial Domain Knowledge](#financial-domain-knowledge)
- [Data Flow & Pipelines](#data-flow--pipelines)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

### What This Project Does

This codebase implements a **nature-based financial risk analysis system** that quantifies how disruptions to ecosystem services impact financial portfolios. It connects:

1. **Ecosystem science**: Vulnerability of economic sectors to nature degradation
2. **Financial theory**: Merton structural model for credit risk
3. **Portfolio analysis**: Securities holdings statistics (SHS) data

**Key Use Case**: Assess how shocks to ecosystem services (e.g., water flow regulation, pollination, soil retention) propagate through the economy to affect bond and equity prices, ultimately impacting portfolio values.

### Project History

- **Origin**: Jupyter notebook (`shs_nature_analysis_Seb.ipynb`)
- **Refactoring**: Transformed into modular Python codebase with clean architecture
- **Status**: Production-ready with comprehensive testing and validation

### Key Capabilities

- Calculate asset depreciation from ecosystem service disruptions
- Model financial impacts using Merton credit risk framework
- Aggregate portfolio losses across multiple dimensions (sector, geography, instrument type)
- Support multiple scenarios and ecosystem services
- Parallel processing for performance
- Extensive validation against original implementation

---

## Quick Reference

### Entry Points

| Task | Command | Module |
|------|---------|--------|
| Run as package (recommended) | `import shs_nature_analysis as shs` then `shs.run_pipeline()` | `__init__.py` |
| Run full pipeline | `python shs_example_usage.py` (Example 1) | `shs_main_pipeline.py` |
| Run tests | `python shs_test_suite.py` | `shs_test_suite.py` |
| Quick validation | `python shs_quick_compare.py` | `shs_quick_compare.py` |

### Key Files

```
shs-nature-analysis/
├── __init__.py                # 📦 Package initialization & exports
├── shs_config.py              # ⚙️  Configuration (start here for parameters)
├── shs_data_loader.py         # 📊 Data loading and preprocessing
├── shs_vulnerability.py       # 🔢 Vulnerability & depreciation calculations
├── shs_financial.py           # 💰 Financial models (Merton, pricing)
├── shs_main_pipeline.py       # 🚀 Main orchestration pipeline
├── shs_visualization.py       # 📈 Plotting and visualization
├── shs_test_suite.py          # ✅ Comprehensive test suite
├── shs_example_usage.py       # 📚 Six usage examples
├── shs_quick_compare.py       # 🔍 Fast output validation
├── SHS_process.py             # 📜 Original code (reference only)
└── shs_readme.md              # 📖 User documentation
```

### Quick Start

**Option 1: As a Package (Recommended)**
```python
# Simple usage
import shs_nature_analysis as shs
results = shs.run_pipeline()

# Or use the class directly for more control
from shs_nature_analysis import SHSAnalysisPipeline
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

**Option 2: Direct Module Import (Legacy)**
```python
from shs_main_pipeline import SHSAnalysisPipeline

# Run full analysis
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

### Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
```

---

## Package Usage

### Overview

The codebase is now structured as a proper Python package with an `__init__.py` file that exports all main components. This makes it easy to import and use in other projects or notebooks.

### Important: Directory Naming

**The directory name uses hyphens (`shs-nature-analysis`) but Python module names require underscores (`shs_nature_analysis`).** To use this as a package, you have three options:

1. **Rename the directory** (simplest):
   ```bash
   mv shs-nature-analysis shs_nature_analysis
   ```

2. **Create a symbolic link**:
   ```bash
   ln -s shs-nature-analysis shs_nature_analysis
   ```

3. **Use the directory name directly** but import from the current directory (only works if you're already in the package directory)

### Installation

Once you've resolved the naming issue, you can use the package in two ways:

1. **Add parent directory to Python path** (for development):
   ```python
   import sys
   sys.path.insert(0, '/path/to/parent/of/shs_nature_analysis')
   import shs_nature_analysis as shs
   ```

2. **Install as editable package** (recommended):
   ```bash
   cd /path/to/shs_nature_analysis
   pip install -e .
   ```
   (Note: This requires a `setup.py` or `pyproject.toml` file - see below)

### Basic Usage

**Simplest approach:**
```python
import shs_nature_analysis as shs

# Run the complete pipeline with one function
results = shs.run_pipeline()
print(f"Analysis complete! Shape: {results.shape}")
```

**With options:**
```python
import shs_nature_analysis as shs

# Run without generating plots
results = shs.run_pipeline(create_plots=False)
```

**Using the pipeline class:**
```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

**Accessing submodules:**
```python
from shs_nature_analysis import config, data_loader, vulnerability, financial, visualization

# Access configuration
print(f"Risk-free rate: {config.RISK_FREE_RATE}")

# Use specific functions
instrument_df = data_loader.load_instrument_data()
```

**Step-by-step execution:**
```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()

# Step 1: Load data
pipeline.load_all_data()
print(f"Loaded {len(pipeline.instrument_df)} instruments")

# Step 2: Calculate depreciations
depreciation_df = pipeline.calculate_instrument_depreciations()

# Step 3: Calculate financial impacts
financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)

# Step 4: Calculate SHS losses
final_results = pipeline.calculate_shs_losses(financial_impacts)
```

### Exported Components

The `__init__.py` file exports the following:

- **`run_pipeline()`**: Convenience function to run the complete analysis
- **`SHSAnalysisPipeline`**: Main pipeline class
- **`config`**: Configuration module (alias for `shs_config`)
- **`data_loader`**: Data loading functions (alias for `shs_data_loader`)
- **`vulnerability`**: Vulnerability calculation functions (alias for `shs_vulnerability`)
- **`financial`**: Financial modeling functions (alias for `shs_financial`)
- **`visualization`**: Plotting functions (alias for `shs_visualization`)

### Package Version

```python
import shs_nature_analysis as shs
print(shs.__version__)  # Output: 1.0.0
```

### Creating a setup.py (Optional)

To install the package properly, create a `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name="shs-nature-analysis",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "joblib>=1.0.0",
        "openpyxl>=3.0.0",
    ],
    python_requires=">=3.8",
    author="SHS Nature Analysis Team",
    description="Nature-based financial risk analysis system",
    long_description=open("shs_readme.md").read(),
    long_description_content_type="text/markdown",
)
```

Then install with:
```bash
pip install -e .
```

---

## Codebase Architecture

### Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined purpose
2. **Type Safety**: Comprehensive type hints throughout
3. **Testability**: Small, focused functions with clear inputs/outputs
4. **Logging**: Comprehensive logging for debugging and monitoring
5. **Error Handling**: Robust validation and fallback mechanisms

### Module Hierarchy

```
┌─────────────────────────────────────┐
│      shs_main_pipeline.py           │ ← Orchestration Layer
│   (SHSAnalysisPipeline class)       │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┬──────────────┬─────────────┐
       ▼               ▼              ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ data_loader  │ │vulnerability │ │financial │ │visualization │ ← Business Logic
└──────────────┘ └──────────────┘ └──────────┘ └──────────────┘
       │               │              │             │
       └───────────────┴──────────────┴─────────────┘
                       │
                ┌──────▼──────┐
                │shs_config.py│ ← Configuration Layer
                └─────────────┘
```

### Data Flow

```
Raw Data Files
    ↓
[shs_data_loader.py] → Load & preprocess
    ↓
Instrument DataFrame + Vulnerability Data + Alpha Shocks
    ↓
[shs_vulnerability.py] → Calculate depreciations (parallel)
    ↓
Depreciation Matrix (instruments × scenarios)
    ↓
[shs_financial.py] → Calculate price variations
    ↓
Financial Impacts DataFrame
    ↓
[shs_main_pipeline.py] → Aggregate losses
    ↓
Final Results CSV + Visualizations
```

---

## Module Guide

### `shs_config.py` - Configuration

**Purpose**: Centralized configuration for all analysis parameters.

**Key Constants**:
```python
RISK_FREE_RATE = 0.02          # Risk-free interest rate
CORRELATION_RHO = 0.1          # Asset correlation
PD_CALIB = 0.0459             # Calibration PD
LGD_CALIB = 0.652             # Calibration LGD
MAX_MATURITY = 30             # Max bond maturity (years)
AGGREG_TYPE = 'SR'            # 'SR' or 'max'
DEPENDENCY_TYPE = 'Vuln_total' # 'Vuln_total' or 'DS_total'
```

**When to Edit**:
- Changing analysis parameters
- Adding new ecosystem services
- Modifying file paths
- Adjusting financial constants

### `shs_data_loader.py` - Data Loading

**Purpose**: Load and preprocess all input data.

**Key Functions**:
- `load_instrument_data()` → DataFrame with financial instruments
- `load_vulnerability_data()` → Ecosystem dependency scores by sector
- `load_alpha_data()` → Shock parameters by scenario/country
- `clean_maturity_data()` → Handle missing/invalid maturities
- `load_nace_mapping()` → EXIOBASE to NACE code conversion

**Data Sources**:
1. Instrument data (CSV): PD, volatility, debt ratios, NACE codes
2. Vulnerability scores (CSV): Dependencies by EXIOBASE sector/region
3. Alpha shocks (Excel): Scenario-specific shock magnitudes
4. NACE mappings (Excel): Sector classification conversions
5. SHS holder data (CSV): Holder-instrument positions

**Important Notes**:
- Missing maturity defaults to median by instrument category
- Wide-format data is reshaped to long format
- Area codes are mapped to standardized country codes

### `shs_vulnerability.py` - Vulnerability Calculations

**Purpose**: Calculate weighted vulnerabilities and asset depreciations.

**Key Functions**:

1. **`compute_weighted_metric()`**
   - Calculates production-weighted averages across EXIOBASE sectors
   - Used for vulnerability and adjustment metrics
   - Pattern: `sum(metric × production) / sum(production)`

2. **`get_adjusted_vulnerability()`**
   - Matches instruments to vulnerability data via NACE codes
   - Tries hierarchical matching (levels 0, -1, -2) for better coverage
   - Returns weighted vulnerability × weighted adjustment

3. **`calculate_depreciation()`**
   - **Formula**: `depreciation = weighted_vuln × weighted_adj × alpha`
   - Runs for each (ecosystem service, scenario) combination
   - Parallel processing via joblib

**Performance**:
- Uses `joblib` with `n_jobs=-1` for all CPU cores
- Typical runtime: ~1-2 minutes for full scenario matrix

### `shs_financial.py` - Financial Models

**Purpose**: Implement Merton structural model and pricing functions.

**Key Functions**:

1. **Distance to Default (DD) Conversions**
   ```python
   pd_to_dd(pd: float) -> float  # DD = -Φ⁻¹(PD)
   dd_to_pd(dd: float) -> float  # PD = Φ(-DD)
   ```

2. **Asset Volatility Derivation**
   ```python
   calculate_asset_volatility(vol, debt_ratio, pd)
   # σ_asset = (σ_equity / Φ(DD)) × (1 - debt_ratio)
   ```

3. **Loss Given Default**
   ```python
   calculate_lgd(pd, pd_calib, lgd_calib, rho)
   # Incorporates correlation and calibration
   ```

4. **Risky Bond Pricing**
   ```python
   calculate_risky_bond_price(pd, lgd, maturity, coupon, risk_free_rate)
   # B = 1 + (c - r - pd×lgd)×(1-e^(-(r+pd)×T))/(r+pd)
   ```

5. **Price Variations**
   ```python
   calculate_bond_price_variation(...)  # ΔB/B
   calculate_equity_price_variation(...) # ΔS/S (Merton call option)
   ```

**Financial Theory**:
- Merton model: Equity as call option on firm assets
- Credit spread: Incorporates PD × LGD
- Depreciation shock: Reduces distance to default

### `shs_main_pipeline.py` - Pipeline Orchestration

**Purpose**: Coordinate the full analysis workflow.

**Class**: `SHSAnalysisPipeline`

**Methods**:

1. **`load_all_data()`**
   - Loads all input files
   - Validates data integrity
   - Stores in instance variables

2. **`calculate_instrument_depreciations()`**
   - Runs parallel depreciation calculations
   - Returns wide DataFrame: instruments × scenarios

3. **`calculate_financial_impacts()`**
   - Applies Merton model to each instrument
   - Calculates price variations for bonds and equity
   - Returns DataFrame with `price_variation` column

4. **`calculate_shs_losses()`**
   - Merges with holder-instrument data
   - Calculates `VALUE_LOSS = price_variation × position`
   - Aggregates by dimensions

5. **`run_full_pipeline(create_plots=True)`**
   - Executes all steps in sequence
   - Saves intermediate outputs
   - Optional visualization generation
   - Returns final results DataFrame

**Usage Pattern**:
```python
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline()
# or step-by-step:
pipeline.load_all_data()
dep_df = pipeline.calculate_instrument_depreciations()
impacts = pipeline.calculate_financial_impacts(dep_df)
final = pipeline.calculate_shs_losses(impacts)
```

### `shs_visualization.py` - Visualization

**Purpose**: Generate heatmaps and charts for analysis results.

**Key Functions**:

1. **`create_heatmap(data, title, ...)`**
   - Generic heatmap creator
   - Handles missing values, color scales

2. **`plot_production_loss_heatmap(...)`**
   - Shows losses by NACE code × region
   - Used for ecosystem service impact analysis

3. **`plot_loss_heatmap_by_dimension(...)`**
   - Flexible 2D heatmap
   - Configurable dimensions (sector, country, NACE, etc.)
   - Supports percentage or absolute values

4. **`create_summary_statistics(results_df)`**
   - Aggregated metrics by dimension
   - Distribution analysis

**Customization**:
- Edit color schemes in function parameters
- Adjust figure sizes for publication quality
- Export formats: PNG (default), PDF, SVG

### `shs_test_suite.py` - Testing

**Purpose**: Validate refactored code against original implementation.

**Test Categories**:

1. **Unit Tests**
   - `test_financial_functions()`: PD/DD, LGD, pricing formulas
   - `test_vulnerability_calculation()`: Weighted metrics

2. **Integration Tests**
   - `run_integration_tests()`: End-to-end comparison
   - Uses `OutputValidator` class
   - 1% tolerance for numeric differences

3. **Output Validation**
   - Compares CSV outputs column-by-column
   - Statistical summaries (mean, std, min, max)
   - Detailed diff reports

**Running Tests**:
```bash
python shs_test_suite.py  # Full suite with reports
python shs_quick_compare.py  # Fast CSV comparison
```

### `shs_example_usage.py` - Examples

**Six Complete Examples**:

1. **Example 1**: Full pipeline execution
2. **Example 2**: Custom scenario analysis (specific eco-service + scenario)
3. **Example 3**: Sensitivity analysis (vary financial parameters)
4. **Example 4**: Country-specific analysis
5. **Example 5**: Custom visualizations
6. **Example 6**: Data export workflows

**Usage**: Run specific examples by uncommenting in `main()`.

---

## Development Workflows

### Making Changes to the Codebase

#### 1. Configuration Changes

**Scenario**: Change financial parameters or add new ecosystem service.

```python
# Edit shs_config.py
RISK_FREE_RATE = 0.025  # Changed from 0.02
ECO_SERVICES.append('New Ecosystem Service')

# Re-run pipeline
python shs_example_usage.py

# Validate outputs
python shs_test_suite.py
```

#### 2. Adding New Functionality

**Pattern**: Add function → Add tests → Document

```python
# 1. Add function to appropriate module
# shs_financial.py
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
# shs_test_suite.py
def test_new_pricing_model():
    result = new_pricing_model(1.0, 2.0)
    assert abs(result - expected) < 1e-6

# 3. Update this CLAUDE.md file
```

#### 3. Debugging Issues

**Step 1**: Enable detailed logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Step 2**: Run specific pipeline stage
```python
pipeline = SHSAnalysisPipeline()
pipeline.load_all_data()
# Inspect: pipeline.instrument_df, pipeline.vulnerability_df
```

**Step 3**: Use quick comparison for validation
```bash
python shs_quick_compare.py
```

#### 4. Performance Optimization

**Current Bottlenecks**:
- Depreciation calculation (parallelized with joblib)
- Data merging for large datasets

**Optimization Strategies**:
- Adjust `n_jobs` in `calculate_depreciation()` calls
- Use `category` dtype for repeated string columns
- Filter data early in pipeline

#### 5. Adding New Data Sources

**Pattern**:

1. Add file path to `shs_config.py`:
   ```python
   NEW_DATA_FILE = Path("data/new_data.csv")
   ```

2. Create loader function in `shs_data_loader.py`:
   ```python
   def load_new_data() -> pd.DataFrame:
       """Load and preprocess new data."""
       df = pd.read_csv(config.NEW_DATA_FILE)
       # Preprocessing
       return df
   ```

3. Integrate into `SHSAnalysisPipeline.load_all_data()`:
   ```python
   self.new_data_df = load_new_data()
   ```

---

## Common Tasks

### Task 1: Run Full Analysis

**Using the Package (Recommended):**
```python
import shs_nature_analysis as shs

# Simplest way - runs with defaults
results = shs.run_pipeline()

# Output files created:
# - merged_SHS_instr_vulnxalpha_scenarios_*.csv
# - shs_2024-Q4_results.csv
# - Various heatmap PNGs
```

**Using the Class Directly:**
```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

### Task 2: Analyze Specific Scenario

```python
from shs_nature_analysis import SHSAnalysisPipeline, vulnerability, config

pipeline = SHSAnalysisPipeline()
pipeline.load_all_data()

# Calculate depreciations for single eco-service
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

### Task 3: Custom Visualization

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

### Task 4: Export Specific Results

```python
# Filter results for specific criteria
filtered = results[
    (results['eco_service'] == 'Water flow regulation') &
    (results['HOLDER_AREA'] == 'NL')
]

# Export to Excel with formatting
with pd.ExcelWriter('nl_water_results.xlsx') as writer:
    filtered.to_excel(writer, sheet_name='Results', index=False)
```

### Task 5: Sensitivity Analysis

```python
# Test different PD calibrations
for pd_calib in [0.03, 0.0459, 0.06]:
    # Temporarily override config
    original_pd = config.PD_CALIB
    config.PD_CALIB = pd_calib

    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)

    # Save with identifier
    results.to_csv(f'results_pd_{pd_calib}.csv', index=False)

    # Restore
    config.PD_CALIB = original_pd
```

### Task 6: Compare Two Scenarios

```python
scenario1 = results[results['scenario'] == 'Scenario_A']
scenario2 = results[results['scenario'] == 'Scenario_B']

comparison = scenario1.merge(
    scenario2,
    on=['HOLDER_SECTOR', 'HOLDER_AREA', 'eco_service'],
    suffixes=('_A', '_B')
)

comparison['diff'] = comparison['VALUE_LOSS_A'] - comparison['VALUE_LOSS_B']
comparison['diff_pct'] = (comparison['diff'] / comparison['VALUE_LOSS_A']) * 100

print(comparison.nlargest(10, 'diff_pct'))
```

---

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual function validation
   - Financial formulas (PD/DD conversions, pricing)
   - Weighted metric calculations
   - Data preprocessing functions

2. **Integration Tests**: End-to-end workflow
   - Compare refactored vs. original outputs
   - Validate pipeline consistency
   - Check output file formats

3. **Validation Tests**: Numeric accuracy
   - 1% tolerance for floating-point comparisons
   - Shape and column consistency
   - Statistical summaries

### Running Tests

```bash
# Full test suite with detailed reports
python shs_test_suite.py

# Quick CSV comparison
python shs_quick_compare.py

# Specific test
python -c "from shs_test_suite import test_financial_functions; test_financial_functions()"
```

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

### Test Data

**Recommendation**: Use small, synthetic datasets for unit tests.

```python
# Example: Create minimal test DataFrame
test_df = pd.DataFrame({
    'ISIN': ['ISIN001', 'ISIN002'],
    'PD': [0.02, 0.05],
    'vol': [0.3, 0.4],
    'debt_ratio': [0.6, 0.7],
    'nace_lvl2': ['A01', 'B05']
})
```

---

## Coding Conventions

### Python Style

- **PEP 8 compliance**: Follow standard Python style guide
- **Line length**: 100 characters (not strict 79)
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Standard library → Third party → Local modules

### Type Hints

**Always include type hints** for function parameters and returns:

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

**Common types**:
- `pd.DataFrame`, `pd.Series`
- `np.ndarray`
- `float`, `int`, `str`, `bool`
- `Optional[T]`, `List[T]`, `Dict[str, T]`
- `Path` (from pathlib)

### Docstrings

**Google style with Args/Returns**:

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

### DataFrame Column Naming

**Preserve source data conventions** where possible:
- ISIN, HOLDER_SECTOR, HOLDER_AREA (uppercase from source)
- eco_service, scenario (lowercase, internal)
- nace_lvl2, resid_mat_yr (lowercase with underscores)

**Adding new columns**:
- Use descriptive names: `price_variation`, not `pv`
- Use lowercase with underscores
- Include units in name if ambiguous: `maturity_years`

### Error Handling

**Pattern**: Validate early, handle gracefully

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
        logger.warning("Empty DataFrame provided, returning empty result")
        return pd.DataFrame()

    # Main logic
    try:
        result = perform_calculation(df)
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
        raise

    return result
```

### Logging

**Use logging module**, not print statements:

```python
import logging
logger = logging.getLogger(__name__)

# Levels
logger.debug("Detailed diagnostic information")
logger.info("General progress information")
logger.warning("Something unexpected but handled")
logger.error("Error that prevents operation")
```

### Constants vs. Magic Numbers

**Bad**:
```python
result = value * 0.652  # What is 0.652?
```

**Good**:
```python
result = value * config.LGD_CALIB  # Clear meaning
```

---

## Financial Domain Knowledge

### Core Concepts

#### 1. Merton Structural Model

**Premise**: Firm equity is a call option on firm assets.

**Key Variables**:
- **V**: Firm asset value
- **D**: Debt face value
- **σ_V**: Asset volatility
- **T**: Debt maturity
- **r**: Risk-free rate

**Equity Value**: E = V × Φ(d₁) - D × e^(-rT) × Φ(d₂)

Where:
- d₁ = [ln(V/D) + (r + σ_V²/2)T] / (σ_V√T)
- d₂ = d₁ - σ_V√T

#### 2. Distance to Default (DD)

**Definition**: Standardized distance from asset value to default threshold.

**Formula**: DD = [ln(V/D) + (μ - σ_V²/2)T] / (σ_V√T)

**Simplified**: DD = -Φ⁻¹(PD)

**Interpretation**:
- DD = 0: Default is equally likely as survival
- DD > 0: Firm is "safe"
- DD < 0: Firm is in distress

#### 3. Probability of Default (PD)

**Definition**: Likelihood of default within time horizon.

**Conversion**: PD = Φ(-DD)

**Calibration**: This codebase uses PD_CALIB = 0.0459 (~4.6% annual default rate).

#### 4. Loss Given Default (LGD)

**Definition**: Fraction of exposure lost if default occurs.

**Formula (in this code)**:
```python
lgd = lgd_calib * sqrt(
    (1 - rho) * norm.cdf(norm.ppf(pd) / sqrt(1-rho)) / pd +
    rho
)
```

**Calibration**: LGD_CALIB = 0.652 (65.2% recovery rate → 34.8% loss rate).

#### 5. Asset Volatility Derivation

**Given**: Equity volatility (σ_E), debt ratio
**Derive**: Asset volatility (σ_V)

**Formula**:
```python
sigma_V = (sigma_E / norm.cdf(DD)) * (1 - debt_ratio)
```

**Logic**: From Black-Scholes, ∂E/∂V = Φ(d₁), so σ_E = (∂E/∂V) × (V/E) × σ_V.

#### 6. Risky Bond Pricing

**Risk-free bond**: B₀ = 1 (par value)

**Risky bond** (with default risk):
```
B = 1 + (c - r - pd×lgd) × [1 - e^(-(r+pd)×T)] / (r + pd)
```

Where:
- c: Coupon rate
- r: Risk-free rate
- pd: Probability of default
- lgd: Loss given default
- T: Maturity

**Credit spread**: cs = pd × lgd

#### 7. Ecosystem Depreciation Shock

**Mechanism**: Nature degradation → Production decline → Firm asset value falls

**Implementation**:
1. Calculate depreciation: `dep = vulnerability × adjustment × alpha_shock`
2. Reduce distance to default: `DD_new = DD - depreciation / σ_V`
3. Convert to PD: `PD_new = Φ(-DD_new)`
4. Calculate new prices with PD_new, LGD_new

### Key Financial Parameters

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Risk-free rate | r | 2% | config.RISK_FREE_RATE |
| Correlation | ρ | 0.1 | config.CORRELATION_RHO |
| Calibration PD | PD* | 4.59% | config.PD_CALIB |
| Calibration LGD | LGD* | 65.2% | config.LGD_CALIB |
| Max maturity | T_max | 30 years | config.MAX_MATURITY |

### Ecosystem Services

**Types Analyzed**:
- Soil and sediment retention
- Water purification
- Water flow regulation
- Pollination
- Climate regulation
- Pest and disease control
- (and others in config.ECO_SERVICES)

**Vulnerability Metrics**:
- **Vuln_total**: Total vulnerability score (0-1 scale)
- **DS_total**: Dependency score (alternative metric)

**Alpha Shocks**:
- Scenario-specific shock magnitudes
- Vary by country and shock type
- Example: "1_World_shock_10perc_02_GOVonNFC" = 10% global shock affecting government holdings

---

## Data Flow & Pipelines

### Input Data Requirements

#### 1. Instrument Data
**File**: `F_511_31_32_instrmnt_nature_2024-Q4_prepped.csv`

**Required Columns**:
- `ISIN`: Unique instrument identifier
- `PD`: Probability of default
- `vol`: Equity volatility
- `debt_ratio`: Debt / (Debt + Equity)
- `nace_lvl0`, `nace_lvl1`, `nace_lvl2`: Sector codes
- `resid_mat_yr`: Residual maturity (years)
- `Security_type`: 'Bonds' or 'Equity'
- `ISSUER_AREA`: Issuer country code

**Optional**:
- `coupon`: Bond coupon rate (defaults to risk-free rate if missing)

#### 2. Vulnerability Data
**File**: `Vuln_final_03_11_2025.csv`

**Required Columns**:
- `eco_serv`: Ecosystem service name
- `scenario`: Scenario identifier
- `region`: EXIOBASE region code
- `sector`: EXIOBASE sector code
- `Vuln_total` or `DS_total`: Vulnerability score
- `Y`: Production value (for weighting)
- `index_weighted`: Adjustment index

#### 3. Alpha Shock Data
**File**: `Alpha_final_03_11_2025.xlsx`

**Required Columns**:
- `Area`: Country code
- `eco_serv`: Ecosystem service
- `[scenario_name]`: Shock magnitude columns (wide format)

**Note**: Reshapes to long format during loading.

#### 4. NACE Mapping
**File**: `EXIOBASE_to_NACElvl2_tab.xlsx`

**Required Columns**:
- `exio_sector_code`: EXIOBASE sector code
- `nace_code_lvl2`: Corresponding NACE code

#### 5. SHS Holder Data
**File**: `F_511_31_32_hldr_instrmnt_2024-Q4_prepped.csv`

**Required Columns**:
- `ISIN`: Instrument identifier (matches instrument data)
- `HOLDER_SECTOR`: Holder sector classification
- `HOLDER_AREA`: Holder country
- `VALUE`: Position value

### Output Data Structure

#### Primary Output: `shs_2024-Q4_results.csv`

**Columns**:
- **Identifiers**: ISIN, HOLDER_SECTOR, HOLDER_AREA, Security_type
- **Grouping**: eco_service, scenario
- **Sector Info**: nace_lvl0, nace_lvl1, nace_lvl2, ISSUER_AREA
- **Financial**: VALUE (position), VALUE_LOSS (loss amount)
- **Metadata**: Other dimensions as needed

**Aggregation Level**: By holder-instrument-scenario combination.

#### Intermediate Output: Depreciation Matrix

**File**: `merged_SHS_instr_vulnxalpha_scenarios_{DEP_TYPE}_{AGGREG_TYPE}.csv`

**Structure**: Wide format
- Rows: Instruments (ISIN)
- Columns: (ecosystem_service, scenario) combinations
- Values: Depreciation percentages

### Processing Steps Detail

#### Step 1: Data Loading
```python
instrument_df = load_instrument_data()        # ~10k instruments
vulnerability_df = load_vulnerability_data()  # ~200k rows
alpha_df = load_alpha_data()                  # ~5k rows
```

#### Step 2: NACE Matching
```python
# Try hierarchical matching
for nace_level_offset in [0, -1, -2]:
    merged = instrument_df.merge(
        vulnerability_df,
        left_on=f'nace_lvl{2+nace_level_offset}',
        right_on='nace_code',
        how='left'
    )
    # Fill missing values with matches at this level
```

#### Step 3: Weighted Vulnerability
```python
weighted_vuln = (
    vulnerability_df.groupby(merge_keys)
    .apply(lambda g: (g['Vuln_total'] * g['Y']).sum() / g['Y'].sum())
)
```

#### Step 4: Apply Alpha Shock
```python
depreciation = weighted_vuln * weighted_adj * alpha_shock
```

#### Step 5: Financial Impact
```python
# For each instrument:
DD_0 = pd_to_dd(PD)
sigma_V = calculate_asset_volatility(vol, debt_ratio, PD)
DD_loss = DD_0 - (depreciation / sigma_V)
PD_loss = dd_to_pd(DD_loss)

# Calculate price changes
if Security_type == 'Bonds':
    price_variation = calculate_bond_price_variation(...)
else:  # Equity
    price_variation = calculate_equity_price_variation(...)
```

#### Step 6: Portfolio Aggregation
```python
# Merge with holder data
results = financial_impacts.merge(holder_df, on='ISIN')
results['VALUE_LOSS'] = results['price_variation'] * results['VALUE']

# Aggregate
final = results.groupby(
    ['HOLDER_SECTOR', 'HOLDER_AREA', 'eco_service', 'scenario', ...]
).agg({'VALUE': 'sum', 'VALUE_LOSS': 'sum'})
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Missing Country in Alpha Data

**Symptom**: Warning message "Country {X} not found in alpha data, using default (NL)"

**Cause**: Alpha shock data doesn't cover all countries.

**Solution**:
- Add country to alpha data file, OR
- Modify default country in `shs_vulnerability.py:calculate_depreciation()`:
  ```python
  if pd.isna(country) or country not in country_list:
      country = 'US'  # Change default here
  ```

#### Issue 2: Low NACE Match Rate

**Symptom**: Many NaN values in depreciation output.

**Cause**: NACE codes in instrument data don't match vulnerability data.

**Solution**:
- Check NACE mapping completeness
- Hierarchical matching already tries levels 0, -1, -2
- Consider adding more EXIOBASE sector mappings

#### Issue 3: Extreme Price Variations

**Symptom**: Price variations > 100% or < -100%

**Cause**:
- Very high volatility combined with large depreciation
- Extreme PD values

**Solution**: Already handled with clipping:
```python
variation = np.clip(variation, -1, 1)
```

**To adjust bounds**:
```python
variation = np.clip(variation, -0.5, 0.5)  # More conservative
```

#### Issue 4: Slow Performance

**Symptom**: Pipeline takes >10 minutes.

**Cause**: Large dataset or single-core processing.

**Solutions**:
1. **Check parallel processing**:
   ```python
   # In shs_vulnerability.py
   n_jobs = -1  # Use all cores
   ```

2. **Filter data early**:
   ```python
   # Analyze subset of scenarios
   scenarios_to_run = ['Scenario_1', 'Scenario_2']
   alpha_df = alpha_df[alpha_df['scenario'].isin(scenarios_to_run)]
   ```

3. **Profile code**:
   ```python
   import cProfile
   cProfile.run('pipeline.run_full_pipeline()', 'profile_stats')
   ```

#### Issue 5: Memory Issues

**Symptom**: Out of memory errors.

**Cause**: Large depreciation matrix or results DataFrame.

**Solutions**:
1. **Process in batches**:
   ```python
   for eco_service in config.ECO_SERVICES:
       # Run pipeline for one service at a time
       results_subset = pipeline.run_full_pipeline(
           eco_services=[eco_service]
       )
       results_subset.to_csv(f'results_{eco_service}.csv')
   ```

2. **Optimize dtypes**:
   ```python
   # Use category for repeated strings
   df['HOLDER_SECTOR'] = df['HOLDER_SECTOR'].astype('category')
   df['eco_service'] = df['eco_service'].astype('category')
   ```

#### Issue 6: Test Failures

**Symptom**: `shs_test_suite.py` reports differences > 1%.

**Cause**:
- Refactored logic differs from original
- Floating-point precision differences
- Random seed differences (if applicable)

**Solution**:
1. **Check specific columns** with failures
2. **Inspect diff report**: Look for patterns (systematic bias vs. random)
3. **Adjust tolerance** if differences are acceptable:
   ```python
   validator = OutputValidator(rtol=0.02)  # 2% tolerance
   ```

#### Issue 7: Missing Data Files

**Symptom**: `FileNotFoundError` when running pipeline.

**Cause**: Data files not in expected locations.

**Solution**:
1. **Check paths** in `shs_config.py`:
   ```python
   INSTRUMENT_FILE = Path("your/actual/path/F_511_*.csv")
   ```

2. **Use absolute paths** if needed:
   ```python
   INSTRUMENT_FILE = Path("/home/user/data/instruments.csv")
   ```

#### Issue 8: Visualization Errors

**Symptom**: Matplotlib errors or blank plots.

**Cause**:
- Missing data for specified dimensions
- Invalid dimension names

**Solution**:
1. **Verify dimension values**:
   ```python
   print(results['eco_service'].unique())
   print(results['HOLDER_SECTOR'].unique())
   ```

2. **Check for data**:
   ```python
   filtered = results[
       (results['eco_service'] == 'Water flow regulation') &
       (results['scenario'] == 'Scenario_1')
   ]
   if filtered.empty:
       print("No data for this combination!")
   ```

### Debugging Checklist

When encountering issues:

- [ ] Check log output for warnings/errors
- [ ] Verify input data files exist and have expected structure
- [ ] Inspect intermediate DataFrames (after each pipeline stage)
- [ ] Run quick comparison to identify which stage fails
- [ ] Check for NaN/Inf values in critical columns
- [ ] Verify configuration parameters are set correctly
- [ ] Ensure dependencies are installed (run `pip list`)
- [ ] Check for sufficient memory and disk space
- [ ] Review recent changes (if codebase was modified)

### Getting Help

**Internal Resources**:
1. Read `shs_readme.md` for user documentation
2. Check `shs_example_usage.py` for usage patterns
3. Review function docstrings for parameter details
4. Examine test suite for expected behavior

**External Resources**:
- Merton model: Academic papers on structural credit risk
- Pandas documentation: https://pandas.pydata.org/docs/
- NumPy/SciPy documentation: https://numpy.org/doc/, https://scipy.org/

---

## Appendix: Quick Reference Tables

### Function Reference

| Function | Module | Purpose |
|----------|--------|---------|
| `load_instrument_data()` | shs_data_loader | Load financial instrument data |
| `load_vulnerability_data()` | shs_data_loader | Load ecosystem vulnerability data |
| `calculate_depreciation()` | shs_vulnerability | Calculate asset depreciation from shocks |
| `compute_weighted_metric()` | shs_vulnerability | Production-weighted averaging |
| `pd_to_dd()` | shs_financial | Convert PD to distance to default |
| `calculate_asset_volatility()` | shs_financial | Derive asset volatility |
| `calculate_lgd()` | shs_financial | Calculate loss given default |
| `calculate_risky_bond_price()` | shs_financial | Price credit-risky bonds |
| `calculate_bond_price_variation()` | shs_financial | Bond price change from shock |
| `calculate_equity_price_variation()` | shs_financial | Equity price change (Merton) |
| `plot_loss_heatmap_by_dimension()` | shs_visualization | Flexible 2D heatmap |
| `create_summary_statistics()` | shs_visualization | Aggregate metrics |

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RISK_FREE_RATE` | float | 0.02 | Annual risk-free rate |
| `CORRELATION_RHO` | float | 0.1 | Asset correlation |
| `PD_CALIB` | float | 0.0459 | Calibration PD |
| `LGD_CALIB` | float | 0.652 | Calibration LGD |
| `MAX_MATURITY` | int | 30 | Max bond maturity (years) |
| `AGGREG_TYPE` | str | 'SR' | 'SR' or 'max' |
| `DEPENDENCY_TYPE` | str | 'Vuln_total' | Vulnerability metric |

### Key DataFrame Columns

#### Instrument Data
- `ISIN`, `PD`, `vol`, `debt_ratio`, `nace_lvl2`, `resid_mat_yr`, `Security_type`, `ISSUER_AREA`

#### Vulnerability Data
- `eco_serv`, `scenario`, `region`, `sector`, `Vuln_total`, `Y`, `index_weighted`

#### Results Data
- `ISIN`, `HOLDER_SECTOR`, `HOLDER_AREA`, `eco_service`, `scenario`, `VALUE`, `VALUE_LOSS`

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-14 | 1.0 | Initial CLAUDE.md creation - comprehensive guide for AI assistants |

---

## Notes for AI Assistants

### When Working with This Codebase:

1. **Always start with `shs_config.py`** to understand current parameters
2. **Use the pipeline class** (`SHSAnalysisPipeline`) rather than calling functions directly
3. **Validate changes** with test suite before considering them complete
4. **Preserve financial accuracy**: These are real-world risk calculations
5. **Document assumptions**: Financial modeling involves many choices
6. **Consider performance**: This code processes large datasets
7. **Maintain modularity**: Keep functions focused and testable
8. **Add logging**: Help users debug issues
9. **Update tests**: When modifying logic, update validation tests
10. **Update this file**: Keep CLAUDE.md current with code changes

### Common Pitfalls to Avoid:

- **Don't break the Merton model**: Financial formulas are mathematically precise
- **Don't ignore NaN values**: Missing data can cascade through pipeline
- **Don't remove validation**: Error checking prevents silent failures
- **Don't change config defaults** without understanding implications
- **Don't skip tests**: Regression testing is critical for financial code
- **Don't optimize prematurely**: Clarity > speed (until profiling shows bottleneck)

### Best Practices:

- **Read before writing**: Understand existing patterns before adding code
- **Test incrementally**: Run tests after each change
- **Log meaningfully**: Help future debuggers (including yourself)
- **Document domain knowledge**: Financial concepts are not intuitive
- **Preserve provenance**: Keep links to original implementation for comparison

---

**End of CLAUDE.md**
