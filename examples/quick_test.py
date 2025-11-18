"""
Quick Test Example for Nature Analysis Package

This example demonstrates the lightweight quick test functionality that
processes a limited subset of data for fast testing and demonstration.

Use this when you need to:
- Test your installation quickly
- Demonstrate the workflow without waiting
- Validate changes during development
- Get familiar with the package
"""

import time
import nature_analysis


def example_1_basic_quick_test():
    """
    Example 1: Basic quick test with default settings.

    Processes 100 instruments, first scenario, first ecosystem service.
    """
    print("\n" + "="*70)
    print("Example 1: Basic Quick Test (Default: 100 instruments)")
    print("="*70)

    start_time = time.time()

    # Run quick test with default settings
    results = nature_analysis.run_quick_test()

    elapsed = time.time() - start_time

    print(f"\n✓ Quick test completed in {elapsed:.1f} seconds!")
    print(f"✓ Processed {len(results)} instruments")
    print(f"\nResults shape: {results.shape}")
    print(f"\nColumns: {list(results.columns)}")

    # Extract depreciation column (last column)
    depr_col = results.columns[-1]
    print(f"\nDepreciation statistics for '{depr_col}':")
    print(results[depr_col].describe())

    return results


def example_2_custom_size():
    """
    Example 2: Quick test with custom number of instruments.

    Shows how to test with even fewer instruments for ultra-fast testing.
    """
    print("\n" + "="*70)
    print("Example 2: Quick Test with Custom Size (50 instruments)")
    print("="*70)

    start_time = time.time()

    # Run quick test with only 50 instruments
    results = nature_analysis.run_quick_test(n_instruments=50)

    elapsed = time.time() - start_time

    print(f"\n✓ Quick test completed in {elapsed:.1f} seconds!")
    print(f"✓ Processed {len(results)} instruments")

    # Show sample of results
    print("\nFirst 5 rows:")
    print(results.head())

    return results


def example_3_using_pipeline_class():
    """
    Example 3: Using the AnalysisPipeline class directly for more control.

    Demonstrates step-by-step execution with the lightweight method.
    """
    print("\n" + "="*70)
    print("Example 3: Using Pipeline Class Directly")
    print("="*70)

    # Create pipeline instance
    pipeline = nature_analysis.AnalysisPipeline()

    print("\nStep 1: Loading data...")
    start_time = time.time()
    pipeline.load_all_data()
    load_time = time.time() - start_time
    print(f"✓ Data loaded in {load_time:.1f} seconds")
    print(f"  - Instruments: {len(pipeline.instrmnt_df):,}")
    print(f"  - Scenarios: {len(pipeline.scenarios)}")
    print(f"  - Ecosystem services: {len(pipeline.eco_services)}")

    print("\nStep 2: Running lightweight depreciation calculation...")
    start_time = time.time()
    results = pipeline.calculate_instrument_depreciations_light(n_instruments=100)
    calc_time = time.time() - start_time
    print(f"✓ Depreciation calculated in {calc_time:.1f} seconds")

    # Show which scenario and ecosystem service were used
    depr_col = results.columns[-1]
    print(f"\nDepreciation column: {depr_col}")
    print(f"This represents:")
    print(f"  - Scenario: {pipeline.scenarios[0]}")
    print(f"  - Ecosystem service: {pipeline.eco_services[0]}")

    # Show non-zero depreciations
    non_zero = results[results[depr_col] > 0]
    print(f"\nInstruments with non-zero depreciation: {len(non_zero)} out of {len(results)}")

    if len(non_zero) > 0:
        print(f"Depreciation range: {non_zero[depr_col].min():.6f} to {non_zero[depr_col].max():.6f}")

    return results


def example_4_compare_with_full():
    """
    Example 4: Compare quick test vs full pipeline (conceptual).

    This example shows the difference between quick test and full pipeline.
    Note: We don't actually run the full pipeline here as it takes much longer.
    """
    print("\n" + "="*70)
    print("Example 4: Quick Test vs Full Pipeline Comparison")
    print("="*70)

    # Run quick test
    print("\nRunning QUICK TEST...")
    start_quick = time.time()
    quick_results = nature_analysis.run_quick_test(n_instruments=100)
    quick_time = time.time() - start_quick

    print(f"\n✓ Quick test completed in {quick_time:.1f} seconds")
    print(f"  - Instruments processed: {len(quick_results)}")
    print(f"  - Scenarios: 1")
    print(f"  - Ecosystem services: 1")
    print(f"  - Output columns: {quick_results.shape[1]}")

    # Estimate full pipeline
    pipeline = nature_analysis.AnalysisPipeline()
    pipeline.load_all_data()

    total_instruments = len(pipeline.instrmnt_df)
    total_scenarios = len(pipeline.scenarios)
    total_eco_services = len(pipeline.eco_services)

    # Rough estimate: time scales linearly with instruments and scenario/ES combinations
    estimated_full_time = quick_time * (total_instruments / 100) * total_scenarios * total_eco_services

    print(f"\nFull pipeline would process:")
    print(f"  - Instruments: {total_instruments:,}")
    print(f"  - Scenarios: {total_scenarios}")
    print(f"  - Ecosystem services: {total_eco_services}")
    print(f"  - Total combinations: {total_scenarios * total_eco_services}")
    print(f"  - Estimated time: {estimated_full_time/60:.1f} minutes (actual may vary)")

    print(f"\n💡 Speed improvement: ~{estimated_full_time/quick_time:.0f}x faster with quick test!")

    return quick_results


def main():
    """
    Run all examples.

    Demonstrates different ways to use the quick test functionality.
    """
    print("\n" + "="*70)
    print("NATURE ANALYSIS - QUICK TEST EXAMPLES")
    print("="*70)
    print("\nThese examples show how to use the lightweight quick test functionality")
    print("for fast testing and demonstration purposes.")

    # Run all examples
    example_1_basic_quick_test()
    example_2_custom_size()
    example_3_using_pipeline_class()
    example_4_compare_with_full()

    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Try modifying n_instruments to see performance differences")
    print("  2. Examine the depreciation values for different instruments")
    print("  3. When ready, run the full pipeline with: nature_analysis.run_pipeline()")
    print("\n")


if __name__ == "__main__":
    main()
