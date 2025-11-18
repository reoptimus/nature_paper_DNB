# Pull Request

## Title
Refactor: Remove 'shs_' prefix and reorganize into professional package structure

## Description

### Summary

This PR completely reorganizes the codebase to create a professional, production-ready Python package. All file prefixes have been removed, code has been restructured into logical directories, and documentation has been significantly enhanced.

### 🎯 Major Changes

#### 1. Removed "shs_" Prefix from All Modules
- `shs_config.py` → `config.py`
- `shs_data_loader.py` → `data_loader.py`
- `shs_vulnerability.py` → `vulnerability.py`
- `shs_financial.py` → `financial.py`
- `shs_main_pipeline.py` → `pipeline.py`
- `shs_visualization.py` → `visualization.py`

#### 2. Professional Directory Structure

```
shs-nature-analysis/
├── README.md                    # ⭐ Completely rewritten
├── setup.py                     # 🆕 Pip installation support
├── requirements.txt             # 🆕 Dependency management
│
├── nature_analysis/             # 🆕 Main package
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── vulnerability.py
│   ├── financial.py
│   ├── pipeline.py
│   └── visualization.py
│
├── tests/                       # 🆕 Test suite
│   ├── test_suite.py
│   ├── quick_compare.py
│   └── test_import.py
│
├── examples/                    # 🆕 Usage examples
│   ├── basic_usage.py
│   └── advanced_usage.py
│
└── legacy/                      # 🆕 Reference code
    └── SHS_process.py
```

#### 3. Simplified API

**Before:**
```python
from shs_nature_analysis import SHSAnalysisPipeline
pipeline = SHSAnalysisPipeline()
```

**After:**
```python
from nature_analysis import AnalysisPipeline
pipeline = AnalysisPipeline()
```

#### 4. Enhanced Documentation

The README.md now includes:
- ✅ Clear quick start examples with expected outputs
- ✅ Input/output specifications for every major function
- ✅ Step-by-step usage examples
- ✅ Installation instructions
- ✅ Configuration guide
- ✅ API reference
- ✅ Data requirements with schemas
- ✅ Financial models documentation

**Example:**
```python
import nature_analysis

results = nature_analysis.run_pipeline()
print(f"Total portfolio value: €{results['OBS_VALUE'].sum():,.0f}")
print(f"Total value loss: €{results['VALUE_LOSS'].sum():,.0f}")
```

#### 5. Easy Installation

```bash
pip install -e .
```

### 📊 What Changed vs What Stayed the Same

**Changed:**
- ✅ File names (removed "shs_" prefix)
- ✅ Directory organization (professional structure)
- ✅ Class names (`AnalysisPipeline`)
- ✅ Import statements (all updated)
- ✅ Documentation (completely rewritten)
- ✅ Package version (v1.0.0 → v2.0.0)

**Stayed the Same:**
- ✅ All core functionality and algorithms
- ✅ Financial models (Merton framework)
- ✅ Data processing logic
- ✅ Configuration parameters
- ✅ Test validation

### 🚀 Benefits

1. **Cleaner codebase** - No redundant "shs_" prefix on every file
2. **Professional structure** - Clear separation of core code, tests, and examples
3. **Better documentation** - Clear input/output examples for all major functions
4. **Easy installation** - Standard `setup.py` with pip support
5. **Simpler API** - More intuitive class and function names
6. **Ready for distribution** - Can be published to PyPI

### 📝 Files Changed

- 21 files reorganized
- All imports updated
- Comprehensive documentation with clear examples
- Professional package structure

### ✅ Checklist

- [x] All modules renamed and organized
- [x] All imports updated
- [x] Package structure validated
- [x] Documentation rewritten with examples
- [x] Changes committed and pushed

### 📦 Version

Bumped to **v2.0.0** to reflect major refactoring

---

**Ready to merge!** This PR transforms the codebase into a professional, production-ready Python package with clear documentation and intuitive structure.
