"""
Financial modeling functions for PD, LGD, and price variations
"""
import numpy as np
from scipy.stats import norm
import config


def pd_to_dd(pd: float) -> float:
    """Convert probability of default to distance to default."""
    return -norm.ppf(pd)


def dd_to_pd(dd: float) -> float:
    """Convert distance to default to probability of default."""
    return norm.cdf(-dd)


def calculate_asset_volatility(dd: float, vol: float, debt_ratio: float) -> float:
    """
    Derive asset volatility from stock price volatility, DD, and debt ratio.
    
    Args:
        dd: Distance to default
        vol: Stock price volatility
        debt_ratio: Debt to total assets ratio
    
    Returns:
        Asset volatility (sigma)
    """
    return (vol / norm.cdf(dd)) * (1 - debt_ratio)


def calculate_dd_with_loss(dd: float, fls: float, sigma: float) -> float:
    """
    Calculate modified distance to default after loss.
    
    Args:
        dd: Original distance to default
        fls: Future loss scenario (depreciation)
        sigma: Asset volatility
    
    Returns:
        Modified distance to default
    """
    return dd - (fls / sigma)


def calculate_lgd(pd: float, 
                 pd_calib: float = config.PD_CALIB,
                 lgd_calib: float = config.LGD_CALIB,
                 rho: float = config.CORRELATION_RHO) -> float:
    """
    Calculate loss given default.
    
    Args:
        pd: Probability of default
        pd_calib: Calibration PD
        lgd_calib: Calibration LGD
        rho: Correlation parameter
    
    Returns:
        Loss given default
    """
    numerator = (norm.ppf(pd_calib * lgd_calib) + 
                 np.sqrt(1 - rho) * norm.ppf(pd) - 
                 norm.ppf(pd_calib))
    denominator = np.sqrt(1 - rho)
    
    return norm.cdf(numerator / denominator) / pd


def calculate_risky_bond_price(duration: float,
                               pd: float,
                               lgd: float,
                               coupon: float = config.COUPON,
                               rff: float = config.RISK_FREE_RATE) -> float:
    """
    Calculate risky bond price.
    
    Args:
        duration: Bond duration in years
        pd: Probability of default
        lgd: Loss given default
        coupon: Coupon rate (% of nominal)
        rff: Risk-free rate
    
    Returns:
        Risky bond price
    """
    rate_sum = rff + pd
    exp_term = np.exp(-rate_sum * duration)
    
    price = 1 + (coupon - rff - pd * lgd) * (1 - exp_term) / rate_sum
    return price


def calculate_bond_price_variation(duration: float,
                                   pd: float,
                                   lgd: float,
                                   coupon: float = config.COUPON,
                                   rff: float = config.RISK_FREE_RATE,
                                   delta_rff: float = config.DELTA_RATE,
                                   delta_pd: float = 0.0,
                                   delta_lgd: float = 0.0) -> float:
    """
    Calculate bond price variation due to changes in PD and LGD.
    
    Returns:
        Percentage price change (clipped to [-1, 1])
    """
    price_initial = calculate_risky_bond_price(duration, pd, lgd, coupon, rff)
    price_final = calculate_risky_bond_price(
        duration, 
        pd + delta_pd, 
        lgd + delta_lgd, 
        coupon, 
        rff + delta_rff
    )
    
    variation = (price_final - price_initial) / price_initial
    return np.clip(variation, -1, 1)


def calculate_equity_price_variation(dd: float,
                                     dd_loss: float,
                                     sigma: float,
                                     r: float = config.RISK_FREE_RATE) -> float:
    """
    Calculate equity price variation using Merton model.
    
    Args:
        dd: Initial distance to default
        dd_loss: Distance to default after loss
        sigma: Asset volatility
        r: Risk-free rate
    
    Returns:
        Percentage price change (clipped to [-1, 1])
    """
    # Initial price components
    initial_numerator = (np.exp(sigma * dd) * norm.cdf(dd) - 
                        np.exp(-r) * norm.cdf(dd - sigma))
    
    # Final price components
    final_numerator = (np.exp(sigma * dd_loss) * norm.cdf(dd_loss) - 
                      np.exp(-r) * norm.cdf(dd_loss - sigma))
    
    variation = (final_numerator / initial_numerator) - 1
    return np.clip(variation, -1, 1)


def calculate_instrument_impacts(df,
                                pd_col='pd',
                                vol_col='vol',
                                debt_ratio_col='debt_ratio',
                                depreciation_col='Depreciation',
                                maturity_col='resid_mat_yr',
                                instr_class_col='INSTR_CLASS',
                                equity_class='F_511'):
    """
    Calculate all financial impacts (PD, LGD, price variations) for instruments.
    
    Args:
        df: DataFrame with instrument data
        Various column names for flexibility
    
    Returns:
        DataFrame with added columns: sigma, lgd, pd_loss, lgd_loss, bp_var, ep_var, p_var
    """
    result = df.copy()
    
    # Calculate asset volatility
    result['sigma'] = calculate_asset_volatility(
        pd_to_dd(result[pd_col]),
        result[vol_col],
        result[debt_ratio_col]
    )
    
    # Calculate initial LGD
    result['lgd'] = calculate_lgd(result[pd_col])
    
    # Calculate PD after loss
    dd_initial = pd_to_dd(result[pd_col])
    dd_after_loss = calculate_dd_with_loss(
        dd_initial,
        -result[depreciation_col],  # Negative because it's a loss
        result['sigma']
    )
    result['pd_loss'] = dd_to_pd(dd_after_loss)
    
    # Calculate LGD after loss
    result['lgd_loss'] = calculate_lgd(result['pd_loss'])
    
    # Calculate bond price variation (for non-equity)
    result['bp_var'] = np.where(
        result[instr_class_col] == equity_class,
        np.nan,
        calculate_bond_price_variation(
            result[maturity_col],
            result[pd_col],
            result['lgd'],
            delta_pd=result['pd_loss'] - result[pd_col],
            delta_lgd=result['lgd_loss'] - result['lgd']
        )
    )
    
    # Calculate equity price variation
    result['ep_var'] = np.where(
        result[instr_class_col] != equity_class,
        np.nan,
        calculate_equity_price_variation(
            dd_initial,
            dd_after_loss,
            result['sigma']
        )
    )
    
    # Combined price variation
    result['p_var'] = np.where(
        result['ep_var'].notna(),
        result['ep_var'],
        result['bp_var']
    )
    
    # Security type label
    result['Security_type'] = np.where(
        result['ep_var'].notna(),
        'Equity',
        'Bonds'
    )
    
    return result
