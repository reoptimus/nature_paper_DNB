"""
Tests for the visualization module (heatmaps and summary statistics).

Uses small, hand-built dataframes matching the two distinct schemas the
module works with:
- the "production-loss" dataframe from pipeline.prepare_production_loss_analysis()
  (columns: eco_serv, Vuln_type, delta_prod/delta_indout, indout, region, NACE Code)
- the SHS/AnaCredit portfolio-loss results from
  SHSAnalysisPipeline.calculate_financial_impacts() (columns: scenario,
  eco_service, VALUE_LOSS, OBS_VALUE, HOLDER_SECTOR, ...)

No DNB access or confidential data is needed to run these tests.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display available in CI/sandboxes
import matplotlib.pyplot as plt
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from nature_analysis import visualization


@pytest.fixture
def production_loss_raw_df():
    """Pre-merge shape expected by plot_production_loss_heatmap() (raw 'NACE Code')."""
    return pd.DataFrame({
        'region': ['NL', 'NL', 'FR', 'FR', 'NL', 'FR'],
        'NACE Code': [1, 20, 2, 20, 3, 20],
        'eco_serv': ['Pollination'] * 6,
        'Vuln_type': ['1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR'] * 6,
        'option': ['SR'] * 6,
        'delta_prod': [-5.0, -1.0, -4.0, -0.5, -6.0, -1.2],
        'indout': [100.0, 200.0, 90.0, 210.0, 105.0, 195.0],
    })


@pytest.fixture
def production_loss_df():
    """Post-merge shape expected by plot_loss_heatmap_by_dimension()/_by_region()
    (the output of pipeline.prepare_production_loss_analysis(), already
    carrying a friendly 'nace_0d_code' column)."""
    return pd.DataFrame({
        'region': ['NL', 'NL', 'FR', 'FR', 'NL', 'FR'],
        'nace_0d_code': ['A', 'C', 'A', 'C', 'A', 'C'],
        'eco_serv': ['Pollination'] * 6,
        'Vuln_type': ['1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR'] * 6,
        'delta_indout': [-5.0, -1.0, -4.0, -0.5, -6.0, -1.2],
        'indout': [100.0, 200.0, 90.0, 210.0, 105.0, 195.0],
    })


@pytest.fixture
def nace_map():
    return pd.DataFrame({
        'nace_2d_code': [1, 2, 3, 20],
        'nace_0d_code': ['A', 'A', 'A', 'C'],
    })


@pytest.fixture
def portfolio_results_df():
    return pd.DataFrame({
        'HOLDER_SECTOR': ['Financial Corporations', 'Financial Corporations',
                          'Households', 'Households'],
        'nace_lvl1': ['A', 'C', 'A', 'C'],
        'scenario': ['1_World_shock_10perc_02_GOVonNFC'] * 4,
        'eco_service': ['Pollination'] * 4,
        'VALUE_LOSS': [-500_000.0, -50_000.0, -200_000.0, -20_000.0],
        'OBS_VALUE': [10_000_000.0, 5_000_000.0, 4_000_000.0, 3_000_000.0],
    })


class TestCreateHeatmap:
    def test_returns_figure(self):
        data = pd.DataFrame({
            'row': ['a', 'a', 'b', 'b'],
            'col': ['x', 'y', 'x', 'y'],
            'value': [1.0, 2.0, 3.0, 4.0],
        })
        fig = visualization.create_heatmap(
            data, 'row', 'col', 'value',
            title='t', xlabel='x', ylabel='y'
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestProductionLossHeatmap:
    def test_relative(self, production_loss_raw_df, nace_map):
        fig = visualization.plot_production_loss_heatmap(
            production_loss_raw_df,
            eco_service='Pollination',
            vuln_type='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            option='SR',
            country_list=['NL', 'FR'],
            nace_map=nace_map,
            value_type='relative',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_absolute_and_csv_output(self, production_loss_raw_df, nace_map, tmp_path):
        output_path = tmp_path / 'production_loss.csv'
        fig = visualization.plot_production_loss_heatmap(
            production_loss_raw_df,
            eco_service='Pollination',
            vuln_type='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            option='SR',
            country_list=['NL', 'FR'],
            nace_map=nace_map,
            value_type='absolute',
            output_path=output_path,
        )
        assert isinstance(fig, plt.Figure)
        assert output_path.exists()
        plt.close(fig)


class TestLossHeatmapByDimension:
    def test_percentage(self, production_loss_df):
        fig = visualization.plot_loss_heatmap_by_dimension(
            production_loss_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            dimension_x='region',
            dimension_y='nace_0d_code',
            value_type='percentage',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_absolute_eur(self, production_loss_df):
        # Regression test: this branch used to reference a 'VALUE_LOSS'
        # column that was never aggregated, raising a KeyError.
        fig = visualization.plot_loss_heatmap_by_dimension(
            production_loss_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            dimension_x='region',
            dimension_y='nace_0d_code',
            value_type='absolute_eur',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestLossHeatmapByRegion:
    def test_percentage(self, production_loss_df):
        fig = visualization.plot_loss_heatmap_by_region(
            production_loss_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            dimension_x='nace_0d_code',
            region_list=['NL', 'FR'],
            value_type='percentage',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_absolute_eur(self, production_loss_df):
        fig = visualization.plot_loss_heatmap_by_region(
            production_loss_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC_Vuln_total_SR',
            dimension_x='nace_0d_code',
            region_list=['NL', 'FR'],
            value_type='absolute_eur',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPortfolioLossHeatmap:
    def test_percentage(self, portfolio_results_df):
        fig = visualization.plot_portfolio_loss_heatmap(
            portfolio_results_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC',
            dimension_x='HOLDER_SECTOR',
            dimension_y='nace_lvl1',
            value_type='percentage',
        )
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_absolute_eur_and_obs_value(self, portfolio_results_df):
        for value_type in ('absolute_eur', 'obs_value'):
            fig = visualization.plot_portfolio_loss_heatmap(
                portfolio_results_df,
                eco_service='Pollination',
                scenario='1_World_shock_10perc_02_GOVonNFC',
                dimension_x='HOLDER_SECTOR',
                dimension_y='nace_lvl1',
                value_type=value_type,
            )
            assert isinstance(fig, plt.Figure)
            plt.close(fig)

    def test_saves_output_file(self, portfolio_results_df, tmp_path):
        output_path = tmp_path / 'heatmap.png'
        visualization.plot_portfolio_loss_heatmap(
            portfolio_results_df,
            eco_service='Pollination',
            scenario='1_World_shock_10perc_02_GOVonNFC',
            dimension_x='HOLDER_SECTOR',
            dimension_y='nace_lvl1',
            output_path=output_path,
        )
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        plt.close('all')


class TestSummaryStatistics:
    def test_columns_and_values(self, portfolio_results_df):
        summary = visualization.create_summary_statistics(portfolio_results_df)

        assert 'Perc_LOSS' in summary.columns
        assert {'scenario', 'eco_service', 'HOLDER_SECTOR'}.issubset(summary.columns)

        fc_row = summary[summary['HOLDER_SECTOR'] == 'Financial Corporations'].iloc[0]
        expected_loss = -500_000.0 + -50_000.0
        expected_value = 10_000_000.0 + 5_000_000.0
        assert fc_row['VALUE_LOSS_sum'] == pytest.approx(expected_loss)
        assert fc_row['Perc_LOSS'] == pytest.approx(100 * expected_loss / expected_value)


class TestCreateVisualizations:
    def test_saves_heatmap(self, portfolio_results_df, tmp_path, monkeypatch):
        from nature_analysis import config
        monkeypatch.setattr(config, 'ANALYSIS_PATH', tmp_path)

        visualization.create_visualizations(
            portfolio_results_df,
            'Pollination',
            '1_World_shock_10perc_02_GOVonNFC',
            dimension_x='HOLDER_SECTOR',
            dimension_y='nace_lvl1',
        )

        saved = list(tmp_path.glob('heatmap_*.png'))
        assert len(saved) == 1
        assert saved[0].stat().st_size > 0
        plt.close('all')

    def test_does_not_raise_on_bad_input(self):
        # create_visualizations() is used as a best-effort side-effect inside
        # run_full_pipeline(create_plots=True); it must never crash the pipeline.
        bad_df = pd.DataFrame({'not_the_right_columns': [1, 2, 3]})
        visualization.create_visualizations(
            bad_df, 'Pollination', 'some_scenario',
            dimension_x='a', dimension_y='b'
        )
