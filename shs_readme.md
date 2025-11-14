# SHS Nature Analysis - Refactored

Clean, modular implementation of the SHS (Securities Holdings Statistics) nature-based financial risk analysis.

## Project Structure

```
.
├── config.py                  # Configuration settings and paths
├── data_loader.py            # Data loading and preprocessing
├── vulnerability_calc.py     # Vulnerability calculations
├── financial_models.py       # Financial risk models (PD, LGD, prices)
├── visualization.py          # Plotting and visualization
├── main_pipeline.py          # Main orchestration pipeline
├── test_pipeline.py          # Testing and validation
├── example_usage.py          # Simple usage examples
└── README.md                 # This file
```

## Features

### Clean Architecture
- **Separation of Concerns**: Each module has a single, well-defined purpose
- **Type Hints**: Functions include type annotations for clarity
- **Logging**: Comprehensive logging throughout the pipeline
- **Error Handling**: Robust error handling and validation

### Modular Components

1. **config.py**: Centralized configuration
   - File paths
   - Analysis parameters
   - Financial constants
   - Visualization defaults

2. **data_loader.py**: Data ingestion
   - Load instrument data
   - Load vulnerability/dependency scores
   - Load alpha shock parameters
   - NACE code mappings
   - Data cleaning utilities

3. **vulnerability_calc.py**: Risk calculations
   - Weighted vulnerability metrics
   - Adjusted vulnerability by NACE hierarchy
   - Parallel depreciation calculations
   - Production-weighted aggregations

4. **financial_models.py**: Financial theory
   - PD/DD conversions (Merton model)
   - Asset volatility derivation
   - LGD calculations
   - Bond pricing (risky bonds)
   - Equity and bond price variations

5. **visualization.py**: Results visualization
   - Generic heatmap creation
   - Production loss heatmaps
   - Multi-dimensional loss analysis
   - Summary statistics

6. **main_pipeline.py**: Orchestration
   - Complete workflow automation
   - Step-by-step logging
   - Intermediate output saving
   - Optional visualization generation

## Installation

```bash
# Required packages
pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
```

## Quick Start

### Basic Usage

```python
from main_pipeline import SHSAnalysisPipeline

# Create and run pipeline
pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

### Custom Analysis

```python
# Load data only
pipeline = SHSAnalysisPipeline()
pipeline.load_all_data()

# Calculate depreciations for specific scenarios
depreciation_df = pipeline.calculate_instrument_depreciations()

# Calculate financial impacts
financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)

# Generate custom visualizations
from visualization import plot_loss_heatmap_by_dimension

fig = plot_loss_heatmap_by_dimension(
    results,
    eco_service='Water flow regulation',
    scenario='1_World_shock_10perc_02_GOVonNFC',
    dimension_x='nace_lvl1',
    dimension_y='HOLDER_SECTOR',
    value_type='percentage'
)
```

## Configuration

Edit `config.py` to customize:

```python
# Analysis parameters
AGGREG_TYPE = 'SR'  # or 'max'
DEPENDENCY_TYPE = 'Vuln_total'  # or 'DS_total'

# Financial parameters
RISK_FREE_RATE = 0.02
PD_CALIB = 0.0459
LGD_CALIB = 0.652

# Ecosystem services to analyze
ECO_SERVICES = [
    'Water flow regulation',
    'Pollination',
    'Water purification',
    # ... add more
]
```

## Testing

Run the test suite to validate outputs:

```bash
python test_pipeline.py
```

The test suite includes:
- **Unit tests**: Individual function validation
- **Integration tests**: Compare outputs with original code
- **Tolerance checking**: Ensures numerical stability

## Key Improvements Over Original

### Code Quality
✓ Modular structure with clear responsibilities  
✓ Consistent naming conventions  
✓ Comprehensive documentation  
✓ Type hints for better IDE support  
✓ Removed code duplication  

### Performance
✓ Optimized data merging  
✓ Parallel processing preserved  
✓ Memory-efficient operations  
✓ Cached intermediate results  

### Maintainability
✓ Easy to extend with new scenarios  
✓ Simple to modify parameters  
✓ Clear error messages  
✓ Logging for debugging  
✓ Testable components  

### Usability
✓ Single command to run full pipeline  
✓ Intermediate outputs saved automatically  
✓ Optional visualization generation  
✓ Progress tracking with logs  

## Output Files

The pipeline generates:

1. **Depreciation data**: 
   - `merged_SHS_instr_vulnxalpha_scenarios_{DEP_TYPE}_{AGGREG_TYPE}.csv`
   - Depreciation values for each instrument/scenario

2. **Final results**:
   - `shs_2024-Q4_results.csv`
   - Aggregated losses by holder, sector, country

3. **Visualizations** (optional):
   - Heatmaps by NACE code and region
   - Loss distributions by dimension
   - Summary statistics

## Workflow

```
1. Load Data
   ├── Instrument data
   ├── Vulnerability scores
   ├── Alpha shock parameters
   └── NACE mappings
   
2. Calculate Depreciations
   ├── Match instruments to NACE codes
   ├── Calculate weighted vulnerabilities
   ├── Apply alpha shocks
   └── Generate depreciation matrix
   
3. Calculate Financial Impacts
   ├── Convert PD to distance to default
   ├── Calculate asset volatility
   ├── Determine LGD
   ├── Calculate price variations
   └── Distinguish bonds vs equity
   
4. Calculate SHS Losses
   ├── Merge with holder data
   ├── Apply price variations
   ├── Aggregate by dimensions
   └── Generate final results
   
5. Visualize (optional)
   └── Create heatmaps and charts
```

## Financial Models

### Merton Model Components

**Distance to Default (DD)**:
- DD = -Φ⁻¹(PD)
- Measures distance from default threshold

**Asset Volatility (σ)**:
- σ = (vol / Φ(DD)) × (1 - debt_ratio)
- Derived from equity volatility

**Loss Given Default (LGD)**:
- Incorporates correlation and calibration parameters
- Accounts for systematic risk factors

**Bond Pricing**:
- Risky bond price includes credit spread
- B = 1 + (c - r - pd×lgd)×(1-e^(-(r+pd)×T))/(r+pd)

**Price Variations**:
- Bonds: Change in risky bond price
- Equity: Merton model call option value change

## Common Issues

### Missing Countries
If a country lacks alpha data, the code defaults to Netherlands (NL) parameters.

### NACE Matching
The code tries matching at multiple hierarchy levels (0, -1, -2) to maximize coverage.

### Maturity Outliers
Extreme maturity values are clipped to 30 years to avoid unrealistic calculations.

### Parallel Processing
Use `n_jobs=-1` for all cores, or specify a number for limited parallelization.

## Contributing

When adding new features:
1. Keep functions focused and single-purpose
2. Add type hints to function signatures
3. Include docstrings with Args/Returns
4. Add logging at key steps
5. Write tests for new functionality
6. Update this README

## License

[Your license here]

## Contact

[Your contact information]
