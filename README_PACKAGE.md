# SHS Nature Analysis - Package Usage Guide

## Overview

This codebase is now structured as a proper Python package with an `__init__.py` file that provides easy import and usage.

## Quick Start

### Step 1: Fix Directory Naming (Important!)

The directory is currently named `shs-nature-analysis` (with hyphens), but Python requires module names to use underscores. Choose one of these solutions:

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

### Step 2: Install Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
```

### Step 3: Use the Package

**Simple usage:**
```python
import sys
sys.path.insert(0, '/path/to/parent/directory')

import shs_nature_analysis as shs
results = shs.run_pipeline()
```

**Using the pipeline class:**
```python
from shs_nature_analysis import SHSAnalysisPipeline

pipeline = SHSAnalysisPipeline()
results = pipeline.run_full_pipeline(create_plots=True)
```

**Accessing submodules:**
```python
from shs_nature_analysis import config, financial, visualization

print(f"Risk-free rate: {config.RISK_FREE_RATE}")

# Use financial functions
dd = financial.pd_to_dd(0.05)
```

## What's Available

The package exports:

- `run_pipeline()` - Convenience function to run the complete analysis
- `SHSAnalysisPipeline` - Main pipeline class
- `config` - Configuration module
- `data_loader` - Data loading functions
- `vulnerability` - Vulnerability calculation functions
- `financial` - Financial modeling functions
- `visualization` - Plotting functions

## Example Scripts

- `example_package_usage.py` - Comprehensive usage examples
- `test_package_import.py` - Test script to verify imports work

## Documentation

See `CLAUDE.md` for comprehensive documentation including:
- Architecture overview
- Module guide
- Common tasks
- Financial domain knowledge
- Troubleshooting

## Version

Current version: 1.0.0

## Notes

- The `__init__.py` file handles all module exports
- Relative imports are used throughout for package compatibility
- All original functionality is preserved
