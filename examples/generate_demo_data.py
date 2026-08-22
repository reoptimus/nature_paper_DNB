#!/usr/bin/env python3
"""
Generate a small synthetic SHS-like instrument + holder dataset.

This is NOT real DNB data - it is entirely fictitious, generated with a
fixed random seed for reproducibility. It exists so that anyone can run
`nature_analysis.run_demo()` and see the full SHS pipeline (depreciation ->
Merton model -> portfolio losses by holder) end to end, without any DNB
Azure access, using the real, non-confidential vulnerability data already
shipped in data/DS_Vuln_update/Vuln_final_store/.

Run with: python examples/generate_demo_data.py
Outputs: data/demo/demo_shs_instruments.csv, data/demo/demo_shs_holders.csv
"""
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Allow running directly (`python examples/generate_demo_data.py`) without an
# editable install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nature_analysis import config

SEED = 42
N_INSTRUMENTS = 300

# A representative spread of NACE level-2 sectors, from highly nature-dependent
# (agriculture, forestry, fishing, mining) to weakly nature-dependent
# (insurance, business services, R&D) - codes taken from the real
# EXIOBASE-to-NACE mapping shipped in data/EXIOBASE_to_NACElvl2_tab.xlsx.
NACE_LVL2_CODES = [1, 2, 3, 6, 10, 15, 20, 29, 45, 50, 60, 65, 69, 72, 85]

HOLDER_SECTORS = [
    'Financial Corporations', 'Insurance Corporations',
    'Investment Funds', 'Households', 'Government'
]
HOLDER_AREAS = ['NL', 'DE', 'FR', 'BE']


def generate_instruments(rng: np.random.Generator) -> pd.DataFrame:
    n_bonds = int(N_INSTRUMENTS * 0.7)
    n_equity = N_INSTRUMENTS - n_bonds
    instr_class = np.array(['F_32'] * n_bonds + ['F_511'] * n_equity)
    rng.shuffle(instr_class)

    identifiers = [f'DEMO{i:06d}' for i in range(N_INSTRUMENTS)]
    issuer_country = rng.choice(config.COUNTRY_LIST, size=N_INSTRUMENTS)
    nace_lvl2 = rng.choice(NACE_LVL2_CODES, size=N_INSTRUMENTS)
    pd_values = np.round(rng.uniform(0.005, 0.08, size=N_INSTRUMENTS), 4)
    vol_values = np.round(rng.uniform(0.15, 0.45, size=N_INSTRUMENTS), 3)
    debt_ratio = np.round(rng.uniform(0.2, 0.7, size=N_INSTRUMENTS), 3)

    resid_mat_yr = np.where(
        instr_class == 'F_32',
        rng.integers(1, 15, size=N_INSTRUMENTS).astype(float),
        np.nan
    )

    return pd.DataFrame({
        'PERIOD': '2024-Q4',
        'IDENTIFIER': identifiers,
        'INSTR_CLASS': instr_class,
        'ISSUER_COUNTRY': issuer_country,
        'pd': pd_values,
        'vol': vol_values,
        'debt_ratio': debt_ratio,
        'nace_lvl4': np.nan,
        'nace_lvl2': nace_lvl2,
        'nace_lvl': 2,
        'resid_mat_yr': resid_mat_yr,
    })


def generate_holders(rng: np.random.Generator, instruments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for identifier in instruments['IDENTIFIER']:
        n_holders = rng.integers(1, 4)
        sectors = rng.choice(HOLDER_SECTORS, size=n_holders, replace=False)
        areas = rng.choice(HOLDER_AREAS, size=n_holders)
        values = rng.uniform(1e5, 5e7, size=n_holders)
        for sector, area, value in zip(sectors, areas, values):
            rows.append({
                'IDENTIFIER': identifier,
                'HOLDER_SECTOR': sector,
                'HOLDER_AREA': area,
                'OBS_VALUE': round(value, 2),
            })
    return pd.DataFrame(rows)


def main():
    rng = np.random.default_rng(SEED)

    instruments = generate_instruments(rng)
    holders = generate_holders(rng, instruments)

    demo_dir = Path(config.DATA_PATH) / 'demo'
    demo_dir.mkdir(parents=True, exist_ok=True)

    instruments_path = demo_dir / 'demo_shs_instruments.csv'
    holders_path = demo_dir / 'demo_shs_holders.csv'

    instruments.to_csv(instruments_path, index=False)
    holders.to_csv(holders_path, index=False)

    print(f"Wrote {len(instruments)} demo instruments to {instruments_path}")
    print(f"Wrote {len(holders)} demo holder records to {holders_path}")


if __name__ == '__main__':
    main()
