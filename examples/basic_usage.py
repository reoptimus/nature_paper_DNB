#!/usr/bin/env python3
"""
Example script demonstrating package usage

NOTE: To use this package, ensure you have the required dependencies:
    pip install pandas numpy scipy matplotlib seaborn joblib openpyxl

The package is now organized as 'nature_analysis'.
"""

def example_1_simple_usage():
    """Simplest way to run the pipeline."""
    print("Example 1: Simple Usage")
    print("=" * 60)

    import nature_analysis

    # One-line execution
    results = nature_analysis.run_pipeline()

    print(f"Analysis complete! Results shape: {results.shape}")
    print("\nFirst few rows:")
    print(results.head())


def example_2_class_usage():
    """Using the pipeline class for more control."""
    print("\nExample 2: Class Usage")
    print("=" * 60)

    from nature_analysis import AnalysisPipeline

    pipeline = AnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)

    print(f"Analysis complete! Results shape: {results.shape}")


def example_3_step_by_step():
    """Step-by-step execution with intermediate access."""
    print("\nExample 3: Step-by-Step Execution")
    print("=" * 60)

    from nature_analysis import AnalysisPipeline

    pipeline = AnalysisPipeline()

    # Step 1: Load data
    print("Loading data...")
    pipeline.load_all_data()
    print(f"  - Loaded {len(pipeline.instrmnt_df)} instruments")
    print(f"  - Loaded {len(pipeline.vuln_df)} vulnerability records")

    # Step 2: Calculate depreciations
    print("\nCalculating depreciations...")
    depreciation_df = pipeline.calculate_instrument_depreciations()
    print(f"  - Depreciation matrix shape: {depreciation_df.shape}")

    # Step 3: Calculate financial impacts
    print("\nCalculating financial impacts...")
    financial_impacts = pipeline.calculate_financial_impacts(depreciation_df)
    print(f"  - Financial impacts shape: {financial_impacts.shape}")

    # Step 4: Calculate SHS losses
    print("\nCalculating SHS losses...")
    final_results = pipeline.calculate_shs_losses(financial_impacts)
    print(f"  - Final results shape: {final_results.shape}")


def example_4_module_access():
    """Accessing individual modules and functions."""
    print("\nExample 4: Module Access")
    print("=" * 60)

    from nature_analysis import config, financial, visualization

    # Access configuration
    print(f"Risk-free rate: {config.RISK_FREE_RATE}")
    print(f"PD calibration: {config.PD_CALIB}")
    print(f"LGD calibration: {config.LGD_CALIB}")

    # Use financial functions
    pd = 0.05
    dd = financial.pd_to_dd(pd)
    print(f"\nPD={pd:.4f} corresponds to DD={dd:.4f}")

    # Check available visualization functions
    print(f"\nVisualization module has:")
    viz_functions = [f for f in dir(visualization) if not f.startswith('_')]
    for func in viz_functions[:5]:  # Show first 5
        print(f"  - {func}")


def example_5_depreciation_calculation():
    """Custom analysis workflow."""
    print("\nExample 5: Depreciation calculation and write")
    print("=" * 60)

    from nature_analysis import (
        pipeline,
        vulnerability,
        config,
        data_loader
    )

    from nature_analysis.pipeline import SHSAnalysisPipeline
    pipeline_SHS = SHSAnalysisPipeline()
    pipeline_SHS.load_all_data()
    pipeline_SHS.instrmnt_df
    # Calculate depreciation for this specific case
    SHS_dep_df = pipeline_SHS.calculate_instrument_depreciations()

    from nature_analysis.pipeline import AnaCreditAnalysisPipeline
    pipeline_anacredit = AnaCreditAnalysisPipeline()
    pipeline_anacredit.load_all_data()
    pipeline_anacredit.instrmnt_df.columns
    # Calculate depreciation for this specific case
    Anacred_dep_df = pipeline_anacredit.calculate_instrument_depreciations()


if __name__ == "__main__":
    import sys

    print("Nature Analysis Package - Usage Examples")
    print("=" * 60)
    print("\nNOTE: This requires renaming the directory or setting up PYTHONPATH")
    print("See script header for details.\n")

    try:
        # Try to import the package
        import nature_analysis
        print(f"✓ Package imported successfully (version {nature_analysis.__version__})")
        print("\nChoose an example to run:")
        print("1. Simple usage")
        print("2. Class usage")
        print("3. Step-by-step execution")
        print("4. Module access (no data needed)")
        print("5. Custom analysis")

    except ImportError as e:
        print(f"✗ Cannot import package: {e}")
        print("\nPlease ensure the package is properly installed.")
        print("From the repository root, run: pip install -e .")
        sys.exit(1)
