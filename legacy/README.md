# Legacy Code (Not Maintained)

This folder holds the **original, pre-refactor implementation** (a flattened
version of the initial `shs_nature_analysis_Seb.ipynb` notebook), kept only
for historical reference and to cross-check outputs against the current
package during the v2.0 refactor.

**Nothing here is imported by `nature_analysis`, none of it is tested, and
none of it is maintained.** If you are looking for the actual package, start
with the root [`README.md`](../README.md) and the `nature_analysis/` package
instead.

| File | What it was |
|------|-------------|
| `SHS_process.py` | Original flattened SHS processing script |
| `DS_functions.py` | Original depreciation/vulnerability functions |
| `COREP_EL_RWA_scratch_notes.txt` | Ad hoc exploration notes for the AnaCredit CET1 workflow (not runnable as-is) |

If you find a discrepancy between this code and `nature_analysis/`, treat
`nature_analysis/` as correct - this folder is not updated when the package
changes.
