"""
Testing suite to validate refactored code produces similar outputs
"""
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Add parent directory to path so we can import the package when run directly
# (e.g. `python tests/test_suite.py` without an editable install).
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutputValidator:
    """Validates outputs between original and refactored code."""
    
    def __init__(self, tolerance_pct: float = 0.01):
        """
        Args:
            tolerance_pct: Acceptable percentage difference (default 1%)
        """
        self.tolerance = tolerance_pct
        self.results = {}
        
    def compare_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                          name: str, key_cols: list = None) -> bool:
        """
        Compare two dataframes and report differences.
        
        Args:
            df1: Original dataframe
            df2: New dataframe
            name: Name for this comparison
            key_cols: Columns to use as keys for merging
        
        Returns:
            True if dataframes match within tolerance
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Comparing: {name}")
        logger.info(f"{'='*60}")
        
        # Shape comparison
        if df1.shape != df2.shape:
            logger.warning(f"Shape mismatch: {df1.shape} vs {df2.shape}")
            self.results[name] = {'status': 'FAIL', 'reason': 'Shape mismatch'}
            return False
        
        logger.info(f"✓ Shape matches: {df1.shape}")
        
        # Column comparison
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        if cols1 != cols2:
            missing_in_new = cols1 - cols2
            extra_in_new = cols2 - cols1
            if missing_in_new:
                logger.warning(f"Columns missing in new: {missing_in_new}")
            if extra_in_new:
                logger.warning(f"Extra columns in new: {extra_in_new}")
            self.results[name] = {'status': 'FAIL', 'reason': 'Column mismatch'}
            return False
        
        logger.info(f"✓ Columns match: {len(cols1)} columns")
        
        # Value comparison for numeric columns
        numeric_cols = df1.select_dtypes(include=[np.number]).columns
        
        if key_cols:
            # Sort and reset index for fair comparison
            df1_sorted = df1.sort_values(key_cols).reset_index(drop=True)
            df2_sorted = df2.sort_values(key_cols).reset_index(drop=True)
        else:
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        
        max_diff_pct = 0
        problematic_cols = []
        
        for col in numeric_cols:
            # Handle NaN values
            mask = df1_sorted[col].notna() & df2_sorted[col].notna()
            
            if not mask.any():
                continue
            
            vals1 = df1_sorted.loc[mask, col]
            vals2 = df2_sorted.loc[mask, col]
            
            # Calculate relative difference
            denominator = np.maximum(np.abs(vals1), 1e-10)
            rel_diff = np.abs(vals1 - vals2) / denominator
            
            max_rel_diff = rel_diff.max()
            mean_rel_diff = rel_diff.mean()
            
            if max_rel_diff > self.tolerance:
                problematic_cols.append({
                    'column': col,
                    'max_diff_pct': max_rel_diff * 100,
                    'mean_diff_pct': mean_rel_diff * 100
                })
                logger.warning(
                    f"  Column '{col}': max diff = {max_rel_diff*100:.4f}%, "
                    f"mean diff = {mean_rel_diff*100:.4f}%"
                )
            
            max_diff_pct = max(max_diff_pct, max_rel_diff)
        
        if problematic_cols:
            logger.warning(f"✗ {len(problematic_cols)} columns exceed tolerance")
            self.results[name] = {
                'status': 'WARN',
                'max_diff_pct': max_diff_pct * 100,
                'problematic_cols': problematic_cols
            }
            return False
        
        logger.info(f"✓ All numeric columns match within {self.tolerance*100}% tolerance")
        logger.info(f"  Maximum difference: {max_diff_pct*100:.6f}%")
        
        self.results[name] = {'status': 'PASS', 'max_diff_pct': max_diff_pct * 100}
        return True
    
    def print_summary(self):
        """Print summary of all comparisons."""
        logger.info(f"\n{'='*60}")
        logger.info("VALIDATION SUMMARY")
        logger.info(f"{'='*60}")
        
        passed = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        warned = sum(1 for r in self.results.values() if r['status'] == 'WARN')
        failed = sum(1 for r in self.results.values() if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.results.values() if r['status'] == 'SKIP')

        for name, result in self.results.items():
            status_symbol = {'PASS': '✓', 'WARN': '⚠', 'FAIL': '✗', 'SKIP': '⏭'}[result['status']]
            logger.info(f"{status_symbol} {name}: {result['status']}")
            if 'max_diff_pct' in result:
                logger.info(f"    Max difference: {result['max_diff_pct']:.6f}%")

        logger.info(f"\nTotal: {passed} passed, {warned} warnings, {failed} failed, {skipped} skipped")


def test_financial_functions():
    """Test individual financial functions."""
    from nature_analysis.financial import (pd_to_dd, dd_to_pd, calculate_asset_volatility,
                                            calculate_lgd, calculate_risky_bond_price,
                                            calculate_bond_price_variation,
                                            calculate_equity_price_variation)

    logger.info("\nTesting financial functions...")

    # Test PD <-> DD conversion
    test_pd = 0.01
    dd = pd_to_dd(test_pd)
    pd_back = dd_to_pd(dd)
    assert abs(test_pd - pd_back) < 1e-10, "PD/DD conversion failed"
    logger.info("✓ PD/DD conversion works")

    # Test asset volatility
    sigma = calculate_asset_volatility(dd=2.0, vol=0.3, debt_ratio=0.5)
    assert sigma > 0, "Asset volatility should be positive"
    logger.info(f"✓ Asset volatility calculation works: {sigma:.4f}")

    # Test LGD
    lgd = calculate_lgd(test_pd)
    assert 0 < lgd < 1, "LGD should be between 0 and 1"
    logger.info(f"✓ LGD calculation works: {lgd:.4f}")

    # Test bond price
    price = calculate_risky_bond_price(duration=5, pd=0.01, lgd=0.5, coupon=0.02, rff=0.02)
    assert price > 0, "Bond price should be positive"
    logger.info(f"✓ Bond price calculation works: {price:.4f}")

    # Test price variations
    bp_var = calculate_bond_price_variation(
        duration=5, pd=0.01, lgd=0.5, delta_pd=0.005, delta_lgd=0.1
    )
    assert -1 <= bp_var <= 1, "Price variation should be in [-1, 1]"
    logger.info(f"✓ Bond price variation works: {bp_var:.4f}")

    # calculate_equity_price_variation takes (pd, delta_pd, sigma), not (dd, dd_loss, sigma)
    initial_pd = dd_to_pd(2.0)
    delta_pd = dd_to_pd(1.8) - initial_pd
    ep_var = calculate_equity_price_variation(pd=initial_pd, delta_pd=delta_pd, sigma=0.2)
    assert -1 <= ep_var <= 1, "Equity variation should be in [-1, 1]"
    logger.info(f"✓ Equity price variation works: {ep_var:.4f}")


def test_vulnerability_calculation():
    """Test vulnerability calculation functions."""
    from nature_analysis.vulnerability import compute_weighted_metric
    
    logger.info("\nTesting vulnerability functions...")
    
    # Create sample data
    test_data = pd.DataFrame({
        'EXIOBASE': ['Sector1', 'Sector2', 'Sector1'],
        'Vuln': [0.1, 0.2, 0.15],
        'indout': [100, 200, 150]
    })
    
    # Test weighted metric
    result = compute_weighted_metric(['Sector1'], test_data, 'Vuln', 'indout')
    expected = (0.1 * 100 + 0.15 * 150) / (100 + 150)
    assert abs(result - expected) < 1e-10, "Weighted metric calculation failed"
    logger.info("✓ Weighted metric calculation works")


def compare_csv_outputs(original_path: str, new_path: str, 
                       validator: OutputValidator, name: str,
                       key_cols: list = None):
    """Helper to compare CSV files."""
    try:
        df_original = pd.read_csv(original_path)
        df_new = pd.read_csv(new_path)
        validator.compare_dataframes(df_original, df_new, name, key_cols)
    except FileNotFoundError as e:
        # These comparison files are only produced by a manual before/after
        # export step (see run_integration_tests docstring) - their absence
        # is expected on a fresh checkout, not a test failure.
        logger.info(f"Skipping '{name}': comparison file not found ({e.filename})")
        validator.results[name] = {'status': 'SKIP', 'reason': 'File not found'}


def run_integration_tests():
    """
    Run integration tests comparing outputs.
    
    Assumes you've run both the original and refactored code
    and saved outputs to compare.
    """
    validator = OutputValidator(tolerance_pct=0.01)  # 1% tolerance
    
    logger.info("\n" + "="*60)
    logger.info("INTEGRATION TESTS")
    logger.info("="*60)
    
    # Compare depreciation outputs
    compare_csv_outputs(
        'merged_SHS_instr_vulnxalpha_scenarios_Vuln_total_SR_ORIGINAL.csv',
        'merged_SHS_instr_vulnxalpha_scenarios_Vuln_total_SR.csv',
        validator,
        'Depreciation Calculations',
        key_cols=['PERIOD', 'IDENTIFIER']
    )
    
    # Compare final SHS results
    compare_csv_outputs(
        'shs_2024-Q4_results_ORIGINAL.csv',
        'shs_2024-Q4_results.csv',
        validator,
        'Final SHS Results',
        key_cols=['HOLDER_SECTOR', 'HOLDER_AREA', 'Scenario', 'Eco_serv']
    )
    
    validator.print_summary()
    return validator


def main():
    """Run all tests."""
    logger.info("Starting test suite...")
    
    # Unit tests
    test_financial_functions()
    test_vulnerability_calculation()
    
    # Integration tests (if files available)
    try:
        validator = run_integration_tests()
        return validator
    except FileNotFoundError:
        logger.warning(
            "\nIntegration tests skipped: comparison files not found. "
            "Run both original and refactored code first."
        )


if __name__ == "__main__":
    main()
