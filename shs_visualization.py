"""
Visualization functions for SHS analysis results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from typing import Optional, Tuple
from . import shs_config as config


def create_heatmap(data: pd.DataFrame,
                  index_col: str,
                  columns_col: str,
                  values_col: str,
                  title: str,
                  xlabel: str,
                  ylabel: str,
                  cmap: str = config.DEFAULT_COLORMAP,
                  figsize: Tuple[int, int] = config.FIGURE_SIZE,
                  annot: bool = False,
                  fmt: str = ".2f",
                  cbar_label: Optional[str] = None) -> plt.Figure:
    """
    Create a generic heatmap from data.
    
    Args:
        data: DataFrame with data to plot
        index_col: Column to use for rows
        columns_col: Column to use for columns
        values_col: Column to use for values
        title: Plot title
        xlabel, ylabel: Axis labels
        cmap: Colormap name
        figsize: Figure size tuple
        annot: Whether to annotate cells
        fmt: Format string for annotations
        cbar_label: Label for colorbar
    
    Returns:
        matplotlib Figure object
    """
    # Pivot data for heatmap
    pivot_data = data.pivot(index=index_col, columns=columns_col, values=values_col)
    pivot_data = pivot_data.fillna(0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    cbar_kws = {'label': cbar_label} if cbar_label else {}
    sns.heatmap(pivot_data, cmap=cmap, cbar_kws=cbar_kws, 
                annot=annot, fmt=fmt, ax=ax, linewidths=0.5)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    
    return fig


def plot_production_loss_heatmap(df: pd.DataFrame,
                                 eco_service: str,
                                 vuln_type: str,
                                 option: str,
                                 country_list: list,
                                 nace_map: pd.DataFrame,
                                 value_type: str = 'relative',
                                 output_path: Optional[str] = None) -> plt.Figure:
    """
    Create heatmap of production losses by NACE code and region.
    
    Args:
        df: Merged dataframe with production loss data
        eco_service: Ecosystem service name
        vuln_type: Vulnerability type
        option: Aggregation option ('SR' or 'max')
        country_list: List of countries to include
        nace_map: NACE mapping dataframe
        value_type: 'relative' for %, 'absolute' for Meur, 'log_absolute' for log scale
        output_path: Optional path to save output CSV
    
    Returns:
        matplotlib Figure object
    """
    # Merge with NACE mapping
    df_merged = df.merge(nace_map, left_on='NACE Code', right_on='nace_2d_code', how='left')
    
    # Filter data
    filtered = df_merged[
        (df_merged['eco_serv'] == eco_service) &
        (df_merged['Vuln_type'] == vuln_type) &
        (df_merged['option'] == option) &
        (df_merged['region'].isin(country_list))
    ]
    
    # Aggregate by region and NACE code
    agg_data = filtered.groupby(['region', 'nace_0d_code'])[
        ['delta_prod', 'indout']
    ].sum().reset_index()
    
    # Calculate relative if needed
    if value_type == 'relative':
        agg_data['value'] = (agg_data['delta_prod'] / agg_data['indout']) * 100
        cbar_label = 'Relative delta_prod (%)'
        title = f"Relative Production Loss by NACE and Region\n({eco_service}, {option})"
    else:
        agg_data['value'] = agg_data['delta_prod']
        cbar_label = 'delta_prod (Meur)'
        title = f"Production Loss in Meur\n({eco_service}, {option})"
    
    # Remove unwanted NACE codes
    agg_data = agg_data[agg_data['nace_0d_code'] != 'U']
    
    # Create heatmap
    if value_type == 'log_absolute':
        # Apply log transformation
        pivot_data = agg_data.pivot(index='nace_0d_code', columns='region', values='value')
        pivot_data = pivot_data.fillna(0)
        heatmap_log = np.log10(-pivot_data + 1e-10)  # Add small constant to avoid log(0)
        
        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
        sns_plot = sns.heatmap(heatmap_log, cmap='BrBG_r', 
                              cbar_kws={'label': cbar_label}, annot=False, ax=ax)
        
        # Format colorbar to show actual values
        colorbar = sns_plot.collections[0].colorbar
        colorbar.ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{10**x:.0f}")
        )
    else:
        fig = create_heatmap(
            agg_data, 'nace_0d_code', 'region', 'value',
            title, 'Region', 'NACE Code',
            cmap='BrBG' if value_type == 'relative' else 'BrBG_r',
            cbar_label=cbar_label
        )
    
    # Save data if requested
    if output_path:
        pivot_data = agg_data.pivot(index='nace_0d_code', columns='region', values='value')
        pivot_data.to_csv(output_path)
    
    return fig


def plot_loss_heatmap_by_dimension(results_df: pd.DataFrame,
                                   eco_service: str,
                                   scenario: str,
                                   dimension_x: str,
                                   dimension_y: str,
                                   value_type: str = 'percentage',
                                   output_path: Optional[str] = None) -> plt.Figure:
    """
    Create heatmap of losses by two dimensions.
    
    Args:
        results_df: SHS results dataframe
        eco_service: Ecosystem service filter
        scenario: Scenario filter
        dimension_x: Column for x-axis (rows)
        dimension_y: Column for y-axis (columns)
        value_type: 'percentage', 'absolute_eur', or 'obs_value'
        output_path: Optional path to save figure
    
    Returns:
        matplotlib Figure object
    """
    # Filter data
    filtered = results_df[
        (results_df['Eco_serv'] == eco_service) &
        (results_df['Scenario'] == scenario)
    ][[dimension_x, dimension_y, 'VALUE_LOSS', 'OBS_VALUE']]
    
    # Aggregate
    agg = filtered.groupby([dimension_x, dimension_y], as_index=False).agg({
        'VALUE_LOSS': 'sum',
        'OBS_VALUE': 'sum'
    })
    agg['Perc_LOSS'] = agg['VALUE_LOSS'] / agg['OBS_VALUE']
    
    # Select value column and formatting
    if value_type == 'percentage':
        value_col = 'Perc_LOSS'
        unit = '%'
        cmap = 'Reds_r'
        annotation_fmt = lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else ""
    elif value_type == 'absolute_eur':
        value_col = 'VALUE_LOSS'
        unit = 'eur'
        cmap = 'Reds_r'
        annotation_fmt = lambda x: f"{x / 1_000_000_000:.2f}b" if pd.notnull(x) else ""
    else:  # obs_value
        value_col = 'OBS_VALUE'
        unit = 'eur'
        cmap = 'Blues'
        annotation_fmt = lambda x: f"{x / 1_000_000_000:.2f}b" if pd.notnull(x) else ""
    
    # Pivot and sort
    pivot_data = agg.pivot(index=dimension_x, columns=dimension_y, values=value_col)
    pivot_data = pivot_data.sort_values(by=pivot_data.columns[0], ascending=True)
    
    # Create annotations
    annotations = pivot_data.map(annotation_fmt)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot_data, annot=annotations, fmt="", cmap=cmap, 
                linewidths=0.5, ax=ax)
    
    title = f"Losses in {unit} by {dimension_x} and {dimension_y}\n({eco_service}, {scenario})"
    ax.set_title(title)
    ax.set_xlabel(dimension_y)
    ax.set_ylabel(dimension_x)
    plt.tight_layout()
    
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_summary_statistics(results_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create summary statistics from results.
    
    Returns:
        DataFrame with summary statistics by scenario, ecosystem service, etc.
    """
    summary = results_df.groupby(['Scenario', 'Eco_serv', 'HOLDER_SECTOR']).agg({
        'VALUE_LOSS': ['sum', 'mean', 'std'],
        'OBS_VALUE': 'sum'
    }).reset_index()
    
    summary.columns = ['_'.join(col).strip('_') for col in summary.columns.values]
    summary['Perc_LOSS'] = (summary['VALUE_LOSS_sum'] / 
                           summary['OBS_VALUE_sum']) * 100
    
    return summary
