"""
Example usage scenarios for the SHS Nature Analysis pipeline
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from main_pipeline import SHSAnalysisPipeline
import config
import visualization


def example_1_full_pipeline():
    """
    Example 1: Run the complete pipeline with default settings
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Complete Pipeline")
    print("="*60)
    
    pipeline = SHSAnalysisPipeline()
    results = pipeline.run_full_pipeline(create_plots=True)
    
    print(f"\nResults shape: {results.shape}")
    print(f"Columns: {list(results.columns)}")
    print(f"\nFirst few rows:")
    print(results.head())
    
    return results


def example_2_custom_scenarios():
    """
    Example 2: Run analysis for specific ecosystem services only
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Scenarios")
    print("="*60)
    
    # Modify config temporarily
    original_services = config.ECO_SERVICES
    config.ECO_SERVICES = ['Water flow regulation', 'Pollination']
    
    try:
        pipeline = SHSAnalysisPipeline()
        pipeline.load_all_data()
        
        print(f"\nAnalyzing {len(config.ECO_SERVICES)} ecosystem services:")
        for es in config.ECO_SERVICES:
            print(f"  - {es}")
        
        depreciation_df = pipeline.calculate_instrument_depreciations()
        print(f"\nDepreciation matrix shape: {depreciation_df.shape}")
        
        return depreciation_df
        
    finally:
        # Restore original config
        config.ECO_SERVICES = original_services


def example_3_custom_visualization():
    """
    Example 3: Create custom visualizations from saved results
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Visualization")
    print("="*60)
    
    # Load previously saved results
    results_file = Path('./shs_2024-Q4_results.csv')
    
    if not results_file.exists():
        print("Results file not found. Run the pipeline first.")
        return
    
    results = pd.read_csv(results_file)
    
    # Create multiple visualizations
    scenarios = ['1_World_shock_10perc_02_GOVonNFC', 
                 '0_World_shock_10perc_02_GOVonNFC']
    eco_services = ['Water flow regulation', 'Pollination']
    
    for scenario in scenarios:
        for eco_service in eco_services:
            if not ((results['Scenario'] == scenario) & 
                   (results['Eco_serv'] == eco_service)).any():
                continue
                
            print(f"\nCreating heatmap: {scenario} - {eco_service}")
            
            fig = visualization.plot_loss_heatmap_by_dimension(
                results,
                eco_service=eco_service,
                scenario=scenario,
                dimension_x='nace_lvl1',
                dimension_y='HOLDER_SECTOR',
                value_type='percentage'
            )
            
            output_name = f"heatmap_{scenario}_{eco_service.replace(' ', '_')}.png"
            fig.savefig(output_name, dpi=300, bbox_inches='tight')
            print(f"  Saved: {output_name}")
            plt.close(fig)


def example_4_sensitivity_analysis():
    """
    Example 4: Compare results with different aggregation types
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Sensitivity Analysis")
    print("="*60)
    
    results_comparison = {}
    
    for aggreg_type in ['SR', 'max']:
        print(f"\nRunning with aggregation type: {aggreg_type}")
        
        # Modify config
        original_aggreg = config.AGGREG_TYPE
        config.AGGREG_TYPE = aggreg_type
        
        try:
            pipeline = SHSAnalysisPipeline()
            pipeline.load_all_data()
            depreciation_df = pipeline.calculate_instrument_depreciations()
            
            # Calculate summary statistics
            depr_cols = [col for col in depreciation_df.columns 
                        if col.startswith('Depr_')]
            summary = depreciation_df[depr_cols].describe()
            
            results_comparison[aggreg_type] = summary
            print(f"\nSummary for {aggreg_type}:")
            print(summary.loc[['mean', 'std', 'min', 'max']])
            
        finally:
            config.AGGREG_TYPE = original_aggreg
    
    # Compare results
    print("\n" + "="*60)
    print("Comparison Summary")
    print("="*60)
    
    for metric in ['mean', 'std']:
        print(f"\n{metric.upper()} comparison:")
        sr_val = results_comparison['SR'].loc[metric].mean()
        max_val = results_comparison['max'].loc[metric].mean()
        diff_pct = ((max_val - sr_val) / sr_val) * 100
        print(f"  SR: {sr_val:.6f}")
        print(f"  max: {max_val:.6f}")
        print(f"  Difference: {diff_pct:.2f}%")


def example_5_analyze_single_country():
    """
    Example 5: Detailed analysis for a single country
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Single Country Analysis")
    print("="*60)
    
    results_file = Path('./shs_2024-Q4_results.csv')
    
    if not results_file.exists():
        print("Results file not found. Run the pipeline first.")
        return
    
    results = pd.read_csv(results_file)
    
    # Analyze Netherlands
    country = 'NL'
    nl_results = results[results['ISSUER_COUNTRY'] == country].copy()
    
    print(f"\nAnalyzing {country}")
    print(f"Total observations: {len(nl_results)}")
    
    # Aggregate by ecosystem service and scenario
    summary = nl_results.groupby(['Eco_serv', 'Scenario']).agg({
        'VALUE_LOSS': 'sum',
        'OBS_VALUE': 'sum'
    }).reset_index()
    
    summary['Loss_Percentage'] = (summary['VALUE_LOSS'] / 
                                  summary['OBS_VALUE']) * 100
    
    print("\nTop 10 scenario/ecosystem service combinations by loss:")
    print(summary.nlargest(10, 'VALUE_LOSS')[
        ['Eco_serv', 'Scenario', 'VALUE_LOSS', 'Loss_Percentage']
    ])
    
    # Plot
    pivot = summary.pivot(index='Eco_serv', columns='Scenario', 
                         values='Loss_Percentage')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind='bar', ax=ax)
    ax.set_title(f'Loss Percentage by Ecosystem Service and Scenario - {country}')
    ax.set_ylabel('Loss %')
    ax.set_xlabel('Ecosystem Service')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_name = f'country_analysis_{country}.png'
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    print(f"\nSaved plot: {output_name}")
    plt.close(fig)


def example_6_export_filtered_data():
    """
    Example 6: Export filtered subsets of data
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Export Filtered Data")
    print("="*60)
    
    results_file = Path('./shs_2024-Q4_results.csv')
    
    if not results_file.exists():
        print("Results file not found. Run the pipeline first.")
        return
    
    results = pd.read_csv(results_file)
    
    # Filter for specific conditions
    filters = {
        'high_risk_bonds': (
            (results['Security_type'] == 'Bonds') & 
            (results['VALUE_LOSS'] < results['VALUE_LOSS'].quantile(0.1))
        ),
        'equity_eurozone': (
            (results['Security_type'] == 'Equity') &
            (results['ISSUER_COUNTRY'].isin(['NL', 'DE', 'FR', 'IT', 'ES']))
        ),
        'water_related': (
            results['Eco_serv'].str.contains('Water', case=False, na=False)
        )
    }
    
    output_dir = Path('./filtered_exports')
    output_dir.mkdir(exist_ok=True)
    
    for name, filter_mask in filters.items():
        filtered_data = results[filter_mask]
        output_file = output_dir / f'{name}.csv'
        filtered_data.to_csv(output_file, index=False)
        print(f"\nExported {len(filtered_data)} rows to {output_file}")
        print(f"  Columns: {list(filtered_data.columns)}")


def main():
    """Run all examples (comment out as needed)"""
    
    print("="*60)
    print("SHS NATURE ANALYSIS - USAGE EXAMPLES")
    print("="*60)
    
    # Run examples (comment out those you don't want)
    
    # Basic usage
    # results = example_1_full_pipeline()
    
    # Advanced usage
    # depreciation_df = example_2_custom_scenarios()
    # example_3_custom_visualization()
    # example_4_sensitivity_analysis()
    # example_5_analyze_single_country()
    # example_6_export_filtered_data()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
