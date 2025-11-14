"""
SHS Nature Analysis Package

A nature-based financial risk analysis system that quantifies how disruptions
to ecosystem services impact financial portfolios.

Quick Start:
    >>> import shs_nature_analysis as shs
    >>> results = shs.run_pipeline()

    # Or use the class directly:
    >>> from shs_nature_analysis import SHSAnalysisPipeline
    >>> pipeline = SHSAnalysisPipeline()
    >>> results = pipeline.run_full_pipeline(create_plots=True)
"""

__version__ = '1.0.0'
__author__ = 'SHS Nature Analysis Team'

# Import main components for easy access
from .shs_main_pipeline import SHSAnalysisPipeline
from . import shs_config as config
from . import shs_data_loader as data_loader
from . import shs_vulnerability as vulnerability
from . import shs_financial as financial
from . import shs_visualization as visualization

# Convenience function for running the full pipeline
def run_pipeline(create_plots=True, **kwargs):
    """
    Run the complete SHS nature analysis pipeline.

    This is a convenience function that creates a pipeline instance
    and runs the full analysis workflow.

    Args:
        create_plots (bool): Whether to generate visualization plots. Default: True
        **kwargs: Additional keyword arguments (reserved for future use)

    Returns:
        pd.DataFrame: Results dataframe with portfolio losses aggregated by
                     holder, instrument type, sector, country, ecosystem service,
                     and scenario.

    Example:
        >>> import shs_nature_analysis as shs
        >>> results = shs.run_pipeline()
        >>> print(results.head())

    Raises:
        FileNotFoundError: If required data files are not found
        ValueError: If data validation fails
    """
    pipeline = SHSAnalysisPipeline()
    return pipeline.run_full_pipeline(create_plots=create_plots)


# Define what gets imported with "from shs_nature_analysis import *"
__all__ = [
    'SHSAnalysisPipeline',
    'run_pipeline',
    'config',
    'data_loader',
    'vulnerability',
    'financial',
    'visualization',
    '__version__',
]
