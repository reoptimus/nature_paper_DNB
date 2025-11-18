# Guide for AI Assistants

> **Context-specific guidance for Claude and other AI assistants working on the Nature-Based Financial Risk Analysis package**

---

## Project Overview

This is a **production-ready financial risk analysis package** for quantifying how ecosystem service disruptions impact financial portfolios through credit risk modeling. The code implements the **Merton structural credit risk framework** with real-world data from central banks.

### Critical Context

- **Domain**: Financial risk modeling + Ecosystem science
- **Stakeholder**: Central banks (DNB - Dutch Central Bank)
- **Data**: Real securities holdings statistics (SHS) data
- **Output**: Portfolio value losses from nature-based risks
- **Precision Required**: High - these are real financial calculations

---

## Priority Guidelines When Working on This Codebase

### 1. **Always Start with Configuration**

Read `nature_analysis/config.py` first to understand:
- Financial parameters (PD_CALIB, LGD_CALIB, RISK_FREE_RATE)
- File paths and data sources
- Analysis settings (AGGREG_TYPE, DEPENDENCY_TYPE)
- Ecosystem services being analyzed

### 2. **Use the Pipeline Class**

Don't call individual functions directly unless there's a specific reason:

```python
# ✓ CORRECT: Use the pipeline
from nature_analysis import AnalysisPipeline
pipeline = AnalysisPipeline()
results = pipeline.run_full_pipeline()

# ✗ AVOID: Direct function calls (unless debugging)
from nature_analysis import vulnerability
dep_df = vulnerability.calculate_depreciation(...)
```

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
- ~50,000 instruments
- Multiple ecosystem services
- Multiple scenarios
- Parallel processing is used extensively

When modifying code, consider:
- Memory usage (DataFrames can be large)
- Computation time (use parallel processing where appropriate)
- Data types (use categorical for repeated strings)

---

## Architecture Overview

### Data Flow

```
Input Files (CSV/Excel)
    ↓
[Data Loader] → Clean, reshape, merge
    ↓
Instrument Data + Vulnerability Scores + Alpha Shocks
    ↓
[Vulnerability Calculator] → Parallel processing by (ecosystem service, scenario)
    ↓
Depreciation Matrix (instruments × scenarios)
    ↓
[Financial Models] → Apply Merton framework
    ↓
Financial Impacts (PD changes, LGD, price variations)
    ↓
[Pipeline Aggregation] → Merge with holder data
    ↓
Final Results CSV (by holder, sector, geography, ecosystem service)
```

### Module Responsibilities

| Module | Primary Purpose | Key Outputs |
|--------|----------------|-------------|
| `config.py` | Centralized parameters | Constants, paths, settings |
| `data_loader.py` | Load and preprocess data | DataFrames (instruments, vulnerability, alpha, holders) |
| `vulnerability.py` | Calculate depreciations | Depreciation matrix (instruments × scenarios) |
| `financial.py` | Financial modeling | PD, LGD, bond prices, equity prices |
| `pipeline.py` | Orchestration | Complete workflow execution |
| `visualization.py` | Plotting | Heatmaps, charts |

### Key Functions Reference

#### Data Loading (`data_loader.py`)
- `load_instrument_data()` - Load financial instruments with risk metrics
- `load_vulnerability_data()` - Load ecosystem vulnerability scores
- `load_alpha_data()` - Load shock parameters
- `load_shs_holder_data()` - Load securities holdings
- `prepare_vulnerability_with_alpha()` - Merge vulnerability and shock data

#### Vulnerability Calculations (`vulnerability.py`)
- `calculate_depreciation()` - Main depreciation calculation for one scenario
- `compute_weighted_metric()` - Production-weighted averaging across sectors
- `calculate_instrument_depreciations_parallel()` - Parallel processing wrapper

#### Financial Models (`financial.py`)
- `pd_to_dd()` - Convert probability of default to distance to default
- `dd_to_pd()` - Convert distance to default to probability of default
- `calculate_asset_volatility()` - Derive asset volatility from equity volatility
- `calculate_lgd()` - Calculate loss given default with correlation
- `calculate_risky_bond_price()` - Price a credit-risky bond
- `calculate_bond_price_variation()` - Price change from PD shock
- `calculate_equity_price_variation()` - Equity price change (Merton model)

#### Pipeline (`pipeline.py`)
- `AnalysisPipeline` class - Main orchestration
  - `load_all_data()` - Load all required files
  - `calculate_instrument_depreciations()` - Calculate depreciation matrix
  - `calculate_financial_impacts()` - Apply Merton model
  - `calculate_shs_losses()` - Aggregate portfolio losses
  - `run_full_pipeline()` - Execute complete workflow

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
2. **Understand current data structure** - read the function first
3. **Make minimal changes** - preserve existing columns unless necessary
4. **Test downstream effects** - check if pipeline still works
5. **Update data requirements** in README.md if schema changes

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
   pipeline = AnalysisPipeline()
   pipeline.load_all_data()
   print(pipeline.instrument_df.head())
   print(pipeline.instrument_df.info())
   ```

3. **Common issues**:
   - Missing NACE codes → Check NACE mapping files
   - Missing countries in alpha data → Check area mapping
   - NaN values → Check merge keys and data completeness
   - Performance issues → Check data volumes and parallelization

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

**WHY:** These parameters are calibrated for specific analysis requirements.

**DO:**
- Ask about the purpose of the parameter
- Run sensitivity analysis to understand impact
- Document why you're changing it

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
def test_full_pipeline():
    """Test complete analysis pipeline."""
    pipeline = AnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)
    assert len(results) > 0
    assert 'VALUE_LOSS' in results.columns
```

### Validation Tests
Compare against reference outputs:
```python
def test_output_matches_reference():
    """Compare outputs with known-good reference."""
    reference_df = pd.read_csv('reference_output.csv')
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

---

## Useful Commands

```bash
# Quick test (fast - use this first!)
python -c "import nature_analysis; nature_analysis.run_quick_test(n_instruments=10)"

# Run quick test examples
python examples/quick_test.py

# Run full test suite
python tests/test_suite.py

# Quick validation
python tests/quick_compare.py

# Test imports
python tests/test_import.py

# Run basic example
python examples/basic_usage.py

# Check package structure
python -c "import nature_analysis; print(dir(nature_analysis))"

# Profile performance
python -m cProfile -o profile.stats examples/basic_usage.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"
```

---

## Summary: Your Workflow

1. **Understand the request** - What's the goal?
2. **Read relevant code** - Don't modify blindly
3. **Check configuration** - What parameters are set?
4. **Make minimal changes** - Preserve existing functionality
5. **Add logging** - Help future debugging
6. **Write tests** - Validate your changes
7. **Run test suite** - Check for regressions
8. **Document changes** - Update README.md if needed
9. **Explain your changes** - Help the user understand what you did

---

## Contact and Escalation

If you encounter:
- **Mathematical questions** about financial models → Ask user for clarification
- **Domain-specific questions** about ecosystem services → Ask user
- **Data availability issues** → Check with user about data sources
- **Conflicting requirements** → Ask user to prioritize

---

**Remember**: This code handles real financial data for central banks. Precision and correctness are more important than speed or cleverness.

---

**Last Updated**: 2025-11-18
**For**: Claude and other AI assistants
**Version**: 2.0.0
