"""
Example: Using Pre-Generated Vulnerability Files

This example demonstrates the STANDARD workflow for running nature-based
financial risk analysis using pre-generated vulnerability and alpha files.

**This is the recommended approach** because:
1. Much faster (no need to regenerate vulnerability data)
2. Uses validated, consistent vulnerability scores
3. Vulnerability data rarely changes unless ENCORE/EXIOBASE updates

**What you need:**
- Vuln_final.csv: Vulnerability scores per region/sector/ecosystem service
- Alpha_final.xlsx: Shock parameters per area/ecosystem service
- SHS instrument data OR AnaCredit instrument data

**Output:**
- Portfolio losses aggregated by holder, sector, geography, ecosystem service

Author: Nature Analysis Team
"""

import nature_analysis
from nature_analysis import config
import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_shs_analysis_with_stored_files():
    """
    Run SHS analysis using pre-generated vulnerability files.

    This is the standard workflow for Securities Holdings Statistics data.
    """
    print("=" * 70)
    print("SHS ANALYSIS WITH PRE-GENERATED VULNERABILITY FILES")
    print("=" * 70)

    print("\n" + "-" * 70)
    print("STEP 1: Verifying vulnerability files")
    print("-" * 70)

    # Check that vulnerability files exist
    vuln_file_path = config.VULN_PATH / config.VULN_FILE
    alpha_file_path = config.VULN_PATH / config.ALPHA_FILE

    if not vuln_file_path.exists():
        print(f"\n✗ Vulnerability file not found: {vuln_file_path}")
        print("\nPlease either:")
        print("1. Place pre-generated Vuln_final.csv in the data directory")
        print("2. Run vulnerability_generation.py to generate new files")
        return

    if not alpha_file_path.exists():
        print(f"\n✗ Alpha file not found: {alpha_file_path}")
        print("\nPlease either:")
        print("1. Place pre-generated Alpha_final.xlsx in the data directory")
        print("2. Run vulnerability_generation.py to generate new files")
        return

    print(f"✓ Vulnerability file: {vuln_file_path}")
    print(f"✓ Alpha file: {alpha_file_path}")

    # Load and inspect vulnerability file
    vuln_df = pd.read_csv(vuln_file_path, nrows=5)
    alpha_df = pd.read_excel(alpha_file_path, nrows=5)

    print(f"\n✓ Vuln file shape: {pd.read_csv(vuln_file_path).shape}")
    print(f"✓ Alpha file shape: {pd.read_excel(alpha_file_path).shape}")
    print(f"✓ Vuln file columns: {list(vuln_df.columns[:8])}...")
    print(f"✓ Alpha file columns: {list(alpha_df.columns)}")

    print("\n" + "-" * 70)
    print("STEP 2: Loading SHS instrument data")
    print("-" * 70)

    # Create pipeline instance
    pipeline = nature_analysis.AnalysisPipeline()

    # Load all data
    try:
        pipeline.load_all_data()
        print(f"\n✓ Loaded {len(pipeline.instrmnt_df)} SHS instruments")
        print(f"✓ Loaded {len(pipeline.scenarios)} scenarios")
        print(f"✓ Loaded {len(pipeline.eco_services)} ecosystem services")
    except FileNotFoundError as e:
        print(f"\n✗ Error loading data: {e}")
        print("\nPlease check config.py paths and ensure all required files exist.")
        return

    print("\n" + "-" * 70)
    print("STEP 3: Calculating instrument depreciations")
    print("-" * 70)
    print("\nThis step:")
    print("1. Merges instrument data with vulnerability scores")
    print("2. Applies alpha shocks per scenario/ecosystem service")
    print("3. Calculates depreciation for each instrument")

    try:
        depreciation_df = pipeline.calculate_instrument_depreciations()
        print(f"\n✓ Calculated depreciations for {len(depreciation_df)} instruments")

        # Show depreciation columns
        depr_cols = [col for col in depreciation_df.columns if col.startswith('Depr_')]
        print(f"✓ Generated {len(depr_cols)} depreciation scenarios")
        if depr_cols:
            print(f"\nExample depreciation column: {depr_cols[0]}")
            print(f"  Min: {depreciation_df[depr_cols[0]].min():.6f}")
            print(f"  Mean: {depreciation_df[depr_cols[0]].mean():.6f}")
            print(f"  Max: {depreciation_df[depr_cols[0]].max():.6f}")

    except Exception as e:
        logger.exception("Error calculating depreciations:")
        print(f"\n✗ Depreciation calculation failed: {e}")
        return

    print("\n" + "-" * 70)
    print("STEP 4: Calculating financial impacts")
    print("-" * 70)
    print("\nApplying Merton credit risk model:")
    print("- PD (Probability of Default) changes")
    print("- LGD (Loss Given Default)")
    print("- Bond and equity price variations")

    try:
        impact_df = pipeline.calculate_financial_impacts(depreciation_df)
        print(f"\n✓ Calculated financial impacts for {len(impact_df)} instrument-scenarios")

        # Show key metrics
        if 'Delta_PD' in impact_df.columns:
            print(f"\nPD changes:")
            print(f"  Mean: {impact_df['Delta_PD'].mean():.6f}")
            print(f"  Max: {impact_df['Delta_PD'].max():.6f}")

        if 'Delta_Price' in impact_df.columns:
            print(f"\nPrice changes:")
            print(f"  Mean: {impact_df['Delta_Price'].mean():.6f}")
            print(f"  Max: {impact_df['Delta_Price'].max():.6f}")

    except Exception as e:
        logger.exception("Error calculating financial impacts:")
        print(f"\n✗ Financial impact calculation failed: {e}")
        return

    print("\n" + "-" * 70)
    print("STEP 5: Aggregating portfolio losses by holder")
    print("-" * 70)

    try:
        results_df = pipeline.calculate_shs_losses(impact_df)
        print(f"\n✓ Aggregated results: {len(results_df)} holder-sector combinations")

        # Summary statistics
        total_value = results_df['OBS_VALUE'].sum()
        total_loss = results_df['VALUE_LOSS'].sum()
        loss_rate = (total_loss / total_value * 100) if total_value > 0 else 0

        print(f"\n{'=' * 70}")
        print("RESULTS SUMMARY")
        print("=" * 70)
        print(f"Total portfolio value: €{total_value:,.0f}")
        print(f"Total value loss: €{total_loss:,.0f}")
        print(f"Loss rate: {loss_rate:.4f}%")

        # Top losses by holder sector
        if 'HOLDER_SECTOR' in results_df.columns:
            print(f"\nTop 5 losses by holder sector:")
            sector_losses = results_df.groupby('HOLDER_SECTOR')['VALUE_LOSS'].sum().sort_values(ascending=False)
            for sector, loss in sector_losses.head(5).items():
                print(f"  {sector}: €{loss:,.0f}")

        # Top losses by ecosystem service
        if 'Eco_serv' in results_df.columns:
            print(f"\nTop 5 losses by ecosystem service:")
            es_losses = results_df.groupby('Eco_serv')['VALUE_LOSS'].sum().sort_values(ascending=False)
            for es, loss in es_losses.head(5).items():
                print(f"  {es}: €{loss:,.0f}")

        print(f"\n✓ Results saved to: {config.RESULTS_PATH}")

        return results_df

    except Exception as e:
        logger.exception("Error aggregating portfolio losses:")
        print(f"\n✗ Portfolio aggregation failed: {e}")
        return


def run_anacredit_analysis_with_stored_files():
    """
    Run AnaCredit analysis using pre-generated vulnerability files.

    This is the standard workflow for bank lending data.
    """
    print("=" * 70)
    print("ANACREDIT ANALYSIS WITH PRE-GENERATED VULNERABILITY FILES")
    print("=" * 70)

    print("\n" + "-" * 70)
    print("STEP 1: Verifying vulnerability files")
    print("-" * 70)

    # Check files exist (same as SHS)
    vuln_file_path = config.VULN_PATH / config.VULN_FILE
    alpha_file_path = config.VULN_PATH / config.ALPHA_FILE

    if not vuln_file_path.exists() or not alpha_file_path.exists():
        print(f"\n✗ Required files not found")
        print("Please run vulnerability_generation.py or place pre-generated files")
        return

    print(f"✓ Vulnerability file: {vuln_file_path}")
    print(f"✓ Alpha file: {alpha_file_path}")

    print("\n" + "-" * 70)
    print("STEP 2: Running AnaCredit pipeline")
    print("-" * 70)

    try:
        # Use the convenience function
        results_df = nature_analysis.run_anacredit_pipeline(create_plots=False)

        print(f"\n{'=' * 70}")
        print("RESULTS SUMMARY")
        print("=" * 70)
        print(f"Processed {len(results_df)} instrument-scenario combinations")

        # Show key columns
        print(f"\nResult columns: {list(results_df.columns)}")

        if 'Delta_PD' in results_df.columns:
            print(f"\nPD changes:")
            print(f"  Mean: {results_df['Delta_PD'].mean():.6f}")
            print(f"  Max: {results_df['Delta_PD'].max():.6f}")

        print(f"\n✓ Results saved to: {config.RESULTS_PATH}")

        return results_df

    except Exception as e:
        logger.exception("Error in AnaCredit pipeline:")
        print(f"\n✗ Analysis failed: {e}")
        return


def main():
    """
    Main function to demonstrate using stored vulnerability files.
    """
    print("\n" + "=" * 70)
    print("NATURE-BASED FINANCIAL RISK ANALYSIS")
    print("Using Pre-Generated Vulnerability Files")
    print("=" * 70)

    print("\nThis example demonstrates the STANDARD workflow:")
    print("1. Use pre-generated Vuln_final.csv and Alpha_final.xlsx")
    print("2. Run financial risk analysis on SHS or AnaCredit data")
    print("3. Calculate portfolio losses")

    print("\nAvailable analyses:")
    print("1. SHS (Securities Holdings Statistics)")
    print("2. AnaCredit (Bank Lending)")
    print("3. Both")

    choice = input("\nSelect analysis (1/2/3) [default: 1]: ").strip() or '1'

    if choice in ['1', '3']:
        print("\n" + "=" * 70)
        print("RUNNING SHS ANALYSIS")
        print("=" * 70)
        shs_results = run_shs_analysis_with_stored_files()

    if choice in ['2', '3']:
        print("\n" + "=" * 70)
        print("RUNNING ANACREDIT ANALYSIS")
        print("=" * 70)
        anacredit_results = run_anacredit_analysis_with_stored_files()

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review results in the output directory")
    print("2. Generate visualizations (see examples/advanced_usage.py)")
    print("3. Export results for reporting")


if __name__ == "__main__":
    main()
