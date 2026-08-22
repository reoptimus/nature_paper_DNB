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
from .pipeline import SHSAnalysisPipeline
from .pipeline import SHSAnalysisPipeline as AnalysisPipeline  # backwards-compatible alias
from .pipeline import AnaCreditAnalysisPipeline
from . import config
from . import data_loader
from . import vulnerability
from . import financial
from . import visualization
from . import vulnerability_generator
from .vulnerability_generator import regenerate_vulnerability_files

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
        - eco_service: Ecosystem service (e.g., 'Water flow regulation')
        - scenario: Shock scenario identifier
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


def run_quick_test(n_instruments=100):
    """
    Run a quick test of the SHS pipeline with limited data.

    This is a lightweight version designed for fast testing and demonstration.
    Uses only:
    - First n_instruments instruments (default: 100)
    - First scenario
    - First ecosystem service

    Args:
        n_instruments (int): Number of instruments to process (default: 100)

    Returns:
        pd.DataFrame: Depreciation results for the limited scenario

    Example:
        >>> import nature_analysis
        >>> results = nature_analysis.run_quick_test(n_instruments=50)
        >>> print(f"Quick test complete! Processed {len(results)} instruments")
        >>> print(f"Depreciation range: {results.iloc[:, -1].min():.4f} to {results.iloc[:, -1].max():.4f}")

    Note:
        This function is much faster than run_pipeline() and is ideal for:
        - Testing the installation
        - Demonstrating the workflow
        - Quick validation during development
    """
    pipeline = AnalysisPipeline()
    return pipeline.run_quick_test(n_instruments=n_instruments)


def run_demo(n_instruments=None):
    """
    Run the SHS pipeline end to end on a synthetic demo dataset - no DNB
    Azure access and no confidential data required.

    The instruments and holders are entirely fictitious (see
    examples/generate_demo_data.py), but the ecosystem-vulnerability data
    driving the results is the real, non-confidential data shipped in
    data/DS_Vuln_update/Vuln_final_store/. This is the easiest way to see
    the whole pipeline (depreciation -> Merton model -> portfolio losses by
    holder) working, e.g. for a first-time user or someone outside DNB.

    Args:
        n_instruments (int, optional): if given, only use the first
            n_instruments demo instruments and the first scenario/ecosystem
            service (faster). If None (default), run on all ~300 demo
            instruments and all configured scenarios/ecosystem services.

    Returns:
        pd.DataFrame: Portfolio losses by holder sector/geography,
        instrument type, ecosystem service and scenario (same shape as
        run_pipeline()).

    Example:
        >>> import nature_analysis
        >>> results = nature_analysis.run_demo()
        >>> print(f"Total (fictitious) loss: €{results['VALUE_LOSS'].sum():,.0f}")
    """
    pipeline = AnalysisPipeline()
    if n_instruments is None:
        return pipeline.run_full_pipeline(demo=True)
    return pipeline.run_quick_test(n_instruments=n_instruments, demo=True)


def run_anacredit_pipeline(create_plots=False, **kwargs):
    """
    Run the complete AnaCredit nature-based financial risk analysis pipeline.

    This convenience function creates an AnaCredit pipeline instance and runs
    the full analysis workflow for AnaCredit instrument data.

    Args:
        create_plots (bool): Whether to generate visualization plots. Default: False
        **kwargs: Additional keyword arguments (reserved for future use)

    Returns:
        pd.DataFrame: Results dataframe with financial impacts including:
                     - Depreciation values
                     - PD (Probability of Default) changes
                     - LGD (Loss Given Default)
                     - Price variations

    Example:
        >>> import nature_analysis
        >>> results = nature_analysis.run_anacredit_pipeline()
        >>> print(f"Processed {len(results)} instrument-scenario combinations")

    Raises:
        FileNotFoundError: If required data files are not found (check config.py)
        ValueError: If data validation fails
    """
    pipeline = AnaCreditAnalysisPipeline()
    return pipeline.run_full_pipeline(create_plots=create_plots)


def run_anacredit_quick_test(n_instruments=100):
    """
    Run a quick test of the AnaCredit pipeline with limited data.

    This is a lightweight version designed for fast testing and demonstration.
    Uses only:
    - First n_instruments instruments (default: 100)
    - First scenario
    - First ecosystem service

    Args:
        n_instruments (int): Number of instruments to process (default: 100)

    Returns:
        pd.DataFrame: Depreciation results for the limited scenario

    Example:
        >>> import nature_analysis
        >>> results = nature_analysis.run_anacredit_quick_test(n_instruments=50)
        >>> print(f"AnaCredit quick test complete! Processed {len(results)} instruments")

    Note:
        This function is much faster than run_anacredit_pipeline() and is ideal for:
        - Testing the AnaCredit data integration
        - Demonstrating the workflow
        - Quick validation during development
    """
    pipeline = AnaCreditAnalysisPipeline()
    return pipeline.run_quick_test(n_instruments=n_instruments)


# Define what gets imported with "from nature_analysis import *"
__all__ = [
    'AnalysisPipeline',
    'SHSAnalysisPipeline',
    'AnaCreditAnalysisPipeline',
    'run_pipeline',
    'run_quick_test',
    'run_demo',
    'run_anacredit_pipeline',
    'run_anacredit_quick_test',
    'regenerate_vulnerability_files',
    'config',
    'data_loader',
    'vulnerability',
    'financial',
    'visualization',
    'vulnerability_generator',
    '__version__',
]
