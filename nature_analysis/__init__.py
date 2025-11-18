"""
Nature-Based Financial Risk Analysis

A production-ready Python package for quantifying how ecosystem service disruptions
impact financial portfolios through credit risk modeling.

Quick Start:
    >>> import nature_analysis
    >>> results = nature_analysis.run_pipeline()

    # Or use the class directly:
    >>> from nature_analysis import AnalysisPipeline
    >>> pipeline = AnalysisPipeline()
    >>> results = pipeline.run_full_pipeline(create_plots=True)
"""

__version__ = '2.0.0'
__author__ = 'Nature Analysis Team'

# Import main components for easy access
from .pipeline import SHSAnalysisPipeline as AnalysisPipeline
from . import config
from . import data_loader
from . import vulnerability
from . import financial
from . import visualization

# Convenience function for running the full pipeline
def run_pipeline(create_plots=True, **kwargs):
    """
    Run the complete nature-based financial risk analysis pipeline.

    This convenience function creates a pipeline instance and runs the full
    analysis workflow.

    Args:
        create_plots (bool): Whether to generate visualization plots. Default: True
        **kwargs: Additional keyword arguments (reserved for future use)

    Returns:
        pd.DataFrame: Results dataframe with portfolio losses aggregated by:
                     - Holder sector and area
                     - Instrument type (bonds/equity)
                     - Issuer sector and country
                     - Ecosystem service
                     - Scenario

    Output Columns:
        - HOLDER_SECTOR: Sector of the security holder
        - HOLDER_AREA: Geographic area of holder
        - Security_type: 'Bonds' or 'Equity'
        - nace_lvl1: NACE economic sector code (level 1)
        - ISSUER_COUNTRY: Country code of security issuer
        - Eco_serv: Ecosystem service (e.g., 'Water flow regulation')
        - Scenario: Shock scenario identifier
        - VALUE_LOSS: Absolute value loss in EUR
        - OBS_VALUE: Original portfolio value in EUR

    Example:
        >>> import nature_analysis
        >>> results = nature_analysis.run_pipeline()
        >>> print(f"Total loss: €{results['VALUE_LOSS'].sum():,.0f}")
        >>> print(f"Loss rate: {(results['VALUE_LOSS'].sum() / results['OBS_VALUE'].sum() * 100):.2f}%")

    Raises:
        FileNotFoundError: If required data files are not found (check config.py)
        ValueError: If data validation fails
    """
    pipeline = AnalysisPipeline()
    return pipeline.run_full_pipeline(create_plots=create_plots)


# Define what gets imported with "from nature_analysis import *"
__all__ = [
    'AnalysisPipeline',
    'run_pipeline',
    'config',
    'data_loader',
    'vulnerability',
    'financial',
    'visualization',
    '__version__',
]
