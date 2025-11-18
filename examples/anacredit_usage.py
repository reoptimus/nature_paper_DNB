#!/usr/bin/env python3
"""
Example script demonstrating AnaCredit data source usage

This script shows how to use the AnaCredit instrument data source
for nature-based financial risk analysis.

NOTE: AnaCredit data must have the same structure as SHS data, including
the same columns (PERIOD, IDENTIFIER, INSTR_CLASS, ISSUER_COUNTRY,
ISSUER_SECTOR, pd, vol, debt_ratio, nace, nace_lvl*, resid_mat_yr, etc.)

Dependencies:
    pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
"""


def example_1_simple_anacredit_usage():
    """Simplest way to run the AnaCredit pipeline."""
    print("Example 1: Simple AnaCredit Usage")
    print("=" * 60)

    import nature_analysis

    # One-line execution for AnaCredit data
    results = nature_analysis.run_anacredit_pipeline()

    print(f"AnaCredit analysis complete! Results shape: {results.shape}")
    print("\nFirst few rows:")
    print(results.head())


def example_2_anacredit_class_usage():
    """Using the AnaCredit pipeline class for more control."""
    print("\nExample 2: AnaCredit Class Usage")
    print("=" * 60)

    from nature_analysis import AnaCreditAnalysisPipeline

    pipeline = AnaCreditAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=False)

    print(f"AnaCredit analysis complete! Results shape: {results.shape}")


def example_3_anacredit_step_by_step():
    """Step-by-step execution with intermediate access."""
    print("\nExample 3: AnaCredit Step-by-Step Execution")
    print("=" * 60)

    from nature_analysis import AnaCreditAnalysisPipeline

    pipeline = AnaCreditAnalysisPipeline()

    # Step 1: Load data
    print("Loading AnaCredit data...")
    pipeline.load_all_data()
    print(f"  - Loaded {len(pipeline.instrmnt_df)} AnaCredit instruments")
    print(f"  - Loaded {len(pipeline.vuln_df)} vulnerability records")

    # Step 2: Calculate depreciations
    print("\nCalculating AnaCredit depreciations...")
    depreciation_df = pipeline.calculate_instrument_depreciations()
    print(f"  - Depreciation matrix shape: {depreciation_df.shape}")

    # Step 3: Calculate financial impacts
    print("\nCalculating AnaCredit financial impacts...")
    financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)
    print(f"  - Financial impacts shape: {financial_impacts.shape}")
    print(f"  - Mean price variation: {financial_impacts['p_var'].mean():.6f}")


def example_4_quick_test_anacredit():
    """Quick test with limited AnaCredit instruments."""
    print("\nExample 4: AnaCredit Quick Test")
    print("=" * 60)

    import nature_analysis

    # Quick test with 50 instruments
    results = nature_analysis.run_anacredit_quick_test(n_instruments=50)

    print(f"Quick test complete! Processed {len(results)} instruments")
    print(f"\nDepreciation column name: {results.columns[-1]}")
    print(f"Depreciation range: {results.iloc[:, -1].min():.6f} to {results.iloc[:, -1].max():.6f}")


def example_5_both_data_sources():
    """Compare SHS and AnaCredit data sources."""
    print("\nExample 5: Comparing SHS and AnaCredit Data Sources")
    print("=" * 60)

    from nature_analysis import AnalysisPipeline, AnaCreditAnalysisPipeline

    # Run SHS pipeline
    print("Running SHS analysis...")
    shs_pipeline = AnalysisPipeline()
    shs_pipeline.load_all_data()
    shs_depr = shs_pipeline.calculate_instrument_depreciations_light(n_instruments=100)
    print(f"  - SHS instruments processed: {len(shs_depr)}")

    # Run AnaCredit pipeline
    print("\nRunning AnaCredit analysis...")
    anacredit_pipeline = AnaCreditAnalysisPipeline()
    anacredit_pipeline.load_all_data()
    anacredit_depr = anacredit_pipeline.calculate_instrument_depreciations_light(n_instruments=100)
    print(f"  - AnaCredit instruments processed: {len(anacredit_depr)}")

    print("\nBoth data sources processed successfully!")
    print("Both use the same calculation methodology with different input data.")


def example_6_using_anacredit_functions_directly():
    """Using AnaCredit-specific functions directly."""
    print("\nExample 6: Using AnaCredit Functions Directly")
    print("=" * 60)

    from nature_analysis import (
        AnaCreditAnalysisPipeline,
        vulnerability,
        config
    )

    pipeline = AnaCreditAnalysisPipeline()
    pipeline.load_all_data()

    # Analyze a specific scenario for AnaCredit
    eco_service = config.ECO_SERVICES[0]  # First ecosystem service
    scenario = pipeline.scenarios[0]  # First scenario

    print(f"Analyzing AnaCredit data for:")
    print(f"  - Ecosystem service: {eco_service}")
    print(f"  - Scenario: {scenario}")

    # Calculate depreciation using AnaCredit wrapper function
    dep_df = vulnerability.calculate_anacredit_depreciation(
        vuln_df=pipeline.vuln_df,
        instrmnt_df=pipeline.instrmnt_df.head(100),  # Limit for demo
        alpha_df=pipeline.alpha_df,
        eco_service=eco_service,
        scenario=scenario,
        option=config.AGGREG_TYPE,
        nace_map=pipeline.nace_map,
        dep_type=config.DEPENDENCY_TYPE
    )

    print(f"\nDepreciation results shape: {dep_df.shape}")
    print(f"Column name: {dep_df.columns[0]}")


if __name__ == "__main__":
    import sys

    print("AnaCredit Nature Analysis - Usage Examples")
    print("=" * 60)
    print("\nThese examples demonstrate how to use AnaCredit instrument data")
    print("for nature-based financial risk analysis.\n")

    try:
        # Try to import the package
        import nature_analysis
        print(f"✓ Package imported successfully (version {nature_analysis.__version__})")
        print("\nAvailable AnaCredit functions:")
        print("  - run_anacredit_pipeline()")
        print("  - run_anacredit_quick_test()")
        print("  - AnaCreditAnalysisPipeline class")
        print("\nChoose an example to run:")
        print("1. Simple AnaCredit usage")
        print("2. AnaCredit class usage")
        print("3. AnaCredit step-by-step execution")
        print("4. AnaCredit quick test")
        print("5. Compare SHS and AnaCredit data sources")
        print("6. Using AnaCredit functions directly")

    except ImportError as e:
        print(f"✗ Cannot import package: {e}")
        print("\nPlease ensure the package is properly installed.")
        print("From the repository root, run: pip install -e .")
        sys.exit(1)
