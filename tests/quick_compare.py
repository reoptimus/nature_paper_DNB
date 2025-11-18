"""
Quick comparison script to validate refactored code outputs
Run this after running both the original and refactored code
"""
import pandas as pd
import numpy as np
from pathlib import Path


def compare_files(original_file: str, new_file: str, tolerance: float = 0.01):
    """
    Compare two CSV files and report differences.
    
    Args:
        original_file: Path to original output
        new_file: Path to new output
        tolerance: Acceptable relative difference (default 1%)
    """
    print(f"\n{'='*70}")
    print(f"Comparing: {Path(original_file).name}")
    print(f"{'='*70}")
    
    try:
        df_orig = pd.read_csv(original_file)
        df_new = pd.read_csv(new_file)
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    
    # Basic checks
    print(f"\n📊 Shape Comparison:")
    print(f"   Original: {df_orig.shape}")
    print(f"   New:      {df_new.shape}")
    
    if df_orig.shape != df_new.shape:
        print("   ⚠️  Shapes don't match!")
        return False
    else:
        print("   ✓ Shapes match")
    
    # Column checks
    print(f"\n📋 Column Comparison:")
    orig_cols = set(df_orig.columns)
    new_cols = set(df_new.columns)
    
    if orig_cols != new_cols:
        missing = orig_cols - new_cols
        extra = new_cols - orig_cols
        if missing:
            print(f"   ⚠️  Missing columns: {missing}")
        if extra:
            print(f"   ⚠️  Extra columns: {extra}")
        return False
    else:
        print(f"   ✓ All {len(orig_cols)} columns match")
    
    # Numeric comparison
    print(f"\n🔢 Numeric Value Comparison:")
    numeric_cols = df_orig.select_dtypes(include=[np.number]).columns
    
    issues = []
    for col in numeric_cols:
        # Get non-null values
        mask = df_orig[col].notna() & df_new[col].notna()
        
        if not mask.any():
            continue
        
        orig_vals = df_orig.loc[mask, col]
        new_vals = df_new.loc[mask, col]
        
        # Calculate differences
        abs_diff = np.abs(orig_vals - new_vals)
        rel_diff = abs_diff / (np.abs(orig_vals) + 1e-10)
        
        max_abs = abs_diff.max()
        max_rel = rel_diff.max()
        mean_rel = rel_diff.mean()
        
        if max_rel > tolerance:
            issues.append({
                'column': col,
                'max_abs_diff': max_abs,
                'max_rel_diff_pct': max_rel * 100,
                'mean_rel_diff_pct': mean_rel * 100,
                'n_samples': len(orig_vals)
            })
    
    if issues:
        print(f"   ⚠️  Found {len(issues)} columns with differences > {tolerance*100}%:")
        for issue in issues[:10]:  # Show top 10
            print(f"\n   Column: {issue['column']}")
            print(f"     Max absolute diff: {issue['max_abs_diff']:.6e}")
            print(f"     Max relative diff: {issue['max_rel_diff_pct']:.4f}%")
            print(f"     Mean relative diff: {issue['mean_rel_diff_pct']:.4f}%")
            print(f"     Samples: {issue['n_samples']}")
    else:
        print(f"   ✓ All numeric columns match within {tolerance*100}% tolerance")
    
    # Sample comparison
    print(f"\n📝 Sample Rows (First 3):")
    print("\nOriginal:")
    print(df_orig.head(3))
    print("\nNew:")
    print(df_new.head(3))
    
    # Summary
    print(f"\n{'='*70}")
    if not issues:
        print("✅ FILES MATCH - Refactored code produces equivalent results!")
    else:
        print("⚠️  DIFFERENCES FOUND - Review the details above")
        if all(i['max_rel_diff_pct'] < tolerance * 10 for i in issues):
            print("   (Differences are small and likely acceptable)")
        else:
            print("   (Some differences are significant)")
    print(f"{'='*70}")
    
    return len(issues) == 0


def quick_stats(file_path: str):
    """Print quick statistics about a results file."""
    print(f"\n{'='*70}")
    print(f"Quick Stats: {Path(file_path).name}")
    print(f"{'='*70}")
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"\n📊 Overview:")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    
    if 'VALUE_LOSS' in df.columns:
        print(f"\n💰 Value Loss Statistics:")
        print(f"   Total: {df['VALUE_LOSS'].sum():,.2f}")
        print(f"   Mean: {df['VALUE_LOSS'].mean():,.2f}")
        print(f"   Median: {df['VALUE_LOSS'].median():,.2f}")
        print(f"   Std: {df['VALUE_LOSS'].std():,.2f}")
    
    if 'OBS_VALUE' in df.columns:
        print(f"\n📈 Observed Value Statistics:")
        print(f"   Total: {df['OBS_VALUE'].sum():,.2f}")
        print(f"   Mean: {df['OBS_VALUE'].mean():,.2f}")
    
    if 'VALUE_LOSS' in df.columns and 'OBS_VALUE' in df.columns:
        pct_loss = (df['VALUE_LOSS'].sum() / df['OBS_VALUE'].sum()) * 100
        print(f"\n📉 Overall Loss Percentage: {pct_loss:.4f}%")
    
    # Group statistics
    if 'Scenario' in df.columns and 'Eco_serv' in df.columns:
        print(f"\n🔍 Scenario Breakdown:")
        print(f"   Scenarios: {df['Scenario'].nunique()}")
        print(f"   Ecosystem Services: {df['Eco_serv'].nunique()}")
        
        top_scenarios = df.groupby(['Scenario', 'Eco_serv'])['VALUE_LOSS'].sum().nlargest(5)
        print(f"\n   Top 5 Scenario/ES by Loss:")
        for (scenario, es), loss in top_scenarios.items():
            print(f"     {scenario[:30]:30s} | {es[:25]:25s} | {loss:,.0f}")


def main():
    """Main comparison workflow."""
    print("="*70)
    print("SHS NATURE ANALYSIS - OUTPUT COMPARISON")
    print("="*70)
    
    # File pairs to compare
    comparisons = [
        {
            'name': 'Depreciation Calculations',
            'original': 'merged_SHS_instr_vulnxalpha_scenarios_Vuln_total_SR_ORIGINAL.csv',
            'new': 'merged_SHS_instr_vulnxalpha_scenarios_Vuln_total_SR.csv'
        },
        {
            'name': 'Final SHS Results',
            'original': 'shs_2024-Q4_results_ORIGINAL.csv',
            'new': 'shs_2024-Q4_results.csv'
        }
    ]
    
    results = {}
    
    for comp in comparisons:
        print(f"\n\n{'#'*70}")
        print(f"# {comp['name']}")
        print(f"{'#'*70}")
        
        # Check if files exist
        orig_exists = Path(comp['original']).exists()
        new_exists = Path(comp['new']).exists()
        
        if not orig_exists:
            print(f"\n⚠️  Original file not found: {comp['original']}")
            print("   Save your original output with '_ORIGINAL' suffix first")
            results[comp['name']] = 'SKIP'
            continue
        
        if not new_exists:
            print(f"\n⚠️  New file not found: {comp['new']}")
            print("   Run the refactored code first")
            results[comp['name']] = 'SKIP'
            continue
        
        # Compare files
        match = compare_files(comp['original'], comp['new'], tolerance=0.01)
        results[comp['name']] = 'PASS' if match else 'DIFF'
    
    # Final summary
    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    
    for name, result in results.items():
        symbol = {'PASS': '✅', 'DIFF': '⚠️', 'SKIP': '⏭️'}[result]
        print(f"{symbol} {name}: {result}")
    
    # Quick stats on new files
    print(f"\n\n{'='*70}")
    print("NEW FILE STATISTICS")
    print(f"{'='*70}")
    
    for comp in comparisons:
        if Path(comp['new']).exists():
            quick_stats(comp['new'])


if __name__ == "__main__":
    main()
