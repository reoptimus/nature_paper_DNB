#!/usr/bin/env python3
"""
Example script demonstrating package usage

NOTE: Before running this script, you need to either:
1. Rename the directory from 'shs-nature-analysis' to 'shs_nature_analysis'
2. Add the parent directory to your PYTHONPATH
3. Create a symbolic link: ln -s shs-nature-analysis shs_nature_analysis

This script assumes you have the required dependencies installed:
    pip install pandas numpy scipy matplotlib seaborn joblib openpyxl
"""

def example_1_simple_usage():
    """Simplest way to run the pipeline."""
    print("Example 1: Simple Usage")
    print("=" * 60)

    import shs_nature_analysis as shs

    # One-line execution
    results = shs.run_pipeline()

    print(f"Analysis complete! Results shape: {results.shape}")
    print("\nFirst few rows:")
    print(results.head())


def example_2_class_usage():
    """Using the pipeline class for more control."""
    print("\nExample 2: Class Usage")
    print("=" * 60)

    from shs_nature_analysis import SHSAnalysisPipeline

    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)

    print(f"Analysis complete! Results shape: {results.shape}")


def example_3_step_by_step():
    """Step-by-step execution with intermediate access."""
    print("\nExample 3: Step-by-Step Execution")
    print("=" * 60)

    from shs_nature_analysis import SHSAnalysisPipeline

    pipeline = SHSAnalysisPipeline()

    # Step 1: Load data
    print("Loading data...")
    pipeline.load_all_data()
    print(f"  - Loaded {len(pipeline.instrument_df)} instruments")
    print(f"  - Loaded {len(pipeline.vulnerability_df)} vulnerability records")

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

    from shs_nature_analysis import config, financial, visualization

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


def example_5_custom_analysis():
    """Custom analysis workflow."""
    print("\nExample 5: Custom Analysis")
    print("=" * 60)

    from shs_nature_analysis import (
        SHSAnalysisPipeline,
        vulnerability,
        config
    )

    pipeline = SHSAnalysisPipeline()
    pipeline.load_all_data()

    # Analyze a specific scenario
    eco_service = 'Water flow regulation'
    scenario = '1_World_shock_10perc_02_GOVonNFC'

    print(f"Analyzing: {eco_service} / {scenario}")

    # Calculate depreciation for this specific case
    dep_df = vulnerability.calculate_depreciation(
        vuln_df=pipeline.vulnerability_df,
        instrmnt_df=pipeline.instrument_df,
        alpha_df=pipeline.alpha_df,
        nace_map_df=pipeline.nace_map_df,
        eco_service=eco_service,
        scenario=scenario,
        dep_type=config.DEPENDENCY_TYPE,
        aggreg_type=config.AGGREG_TYPE,
        nace_level=2
    )

    print(f"Depreciation results shape: {dep_df.shape}")
    print(f"Mean depreciation: {dep_df['Depreciation'].mean():.6f}")
    print(f"Max depreciation: {dep_df['Depreciation'].max():.6f}")


if __name__ == "__main__":
    import sys

    print("SHS Nature Analysis Package - Usage Examples")
    print("=" * 60)
    print("\nNOTE: This requires renaming the directory or setting up PYTHONPATH")
    print("See script header for details.\n")

    try:
        # Try to import the package
        import shs_nature_analysis
        print(f"✓ Package imported successfully (version {shs_nature_analysis.__version__})")
        print("\nChoose an example to run:")
        print("1. Simple usage")
        print("2. Class usage")
        print("3. Step-by-step execution")
        print("4. Module access (no data needed)")
        print("5. Custom analysis")

    except ImportError as e:
        print(f"✗ Cannot import package: {e}")
        print("\nTo fix this, try one of the following:")
        print("1. Rename directory: mv shs-nature-analysis shs_nature_analysis")
        print("2. Create symlink: ln -s shs-nature-analysis shs_nature_analysis")
        print("3. Add to PYTHONPATH: export PYTHONPATH=/path/to/parent:$PYTHONPATH")
        sys.exit(1)
