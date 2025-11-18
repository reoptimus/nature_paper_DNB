# DNB Nature Paper Package

This branch contains the complete nature-based financial risk analysis package
prepared for the DNB_Nature_paper repository.

## Contents

This branch includes:
- ✅ `nature_analysis/` - Complete package with cleaned module names
- ✅ `tests/` - Full test suite
- ✅ `examples/` - Usage examples (basic and advanced)
- ✅ `legacy/` - Original SHS_process.py for reference
- ✅ `setup.py` - Package installation script
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Comprehensive documentation

## Package Features

- Professional structure (no "shs_" prefixes)
- Clean API: `from nature_analysis import AnalysisPipeline`
- Comprehensive documentation with input/output examples
- Easy installation: `pip install -e .`
- Version 2.0.0

## To Use This Code

1. **Clone this branch**:
   ```bash
   git clone -b dnb-nature-paper-package https://github.com/reoptimus/shs-nature-analysis.git
   cd shs-nature-analysis
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Run examples**:
   ```bash
   python examples/basic_usage.py
   ```

## Migration to DNB_Nature_paper

Once the DNB_Nature_paper repository is accessible, you can:

```bash
# In shs-nature-analysis on this branch
git remote add dnb https://github.com/reoptimus/DNB_Nature_paper.git
git push dnb dnb-nature-paper-package:main
```

Or manually copy the files to DNB_Nature_paper repository.

---

**Branch Created**: 2025-11-18
**Package Version**: 2.0.0
**Total Files**: 21 files
