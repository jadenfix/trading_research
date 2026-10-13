import tempfile
import unittest
import numpy as np
from research.native import signals
from research.workbench import run,load_data
from research.backtesting_engine import BacktestingEngine

class NativeResearchTests(unittest.TestCase):
    def test_native_prefix_causality_and_input_rejection(self):
        prices=np.linspace(100,140,64)
        expected=signals(prices)
        changed=prices.copy();changed[40:]=1
        np.testing.assert_array_equal(signals(changed)[:41],expected[:41])
        with self.assertRaises(ValueError): signals([1,float("nan")]*20)
    def test_end_to_end_costed_native_backtest(self):
        with tempfile.TemporaryDirectory() as output:
            report=run(output=output,rows=96)
            self.assertTrue(report['native_reference_match'])
            self.assertGreater(report['trades'],0)
            self.assertGreater(report['commission_paid'],0)
            self.assertTrue(np.isfinite(report['ending_equity']))
    def test_slippage_charged_once(self):
        engine=BacktestingEngine(100000,commission_per_trade=.001,slippage_bps=10)
        trade=engine.execute_trade('X',1,100,'2024-01-01')
        self.assertAlmostEqual(trade['price'],100.1)
        self.assertAlmostEqual(trade['transaction_cost'],100*100.1*.001)
    def test_optional_data_provider_does_not_block_import(self):
        from trading.algorithm import TradingAlgorithm
        from trading.data_fetcher import DataFetcher
        self.assertIsNotNone(DataFetcher())
    def test_zero_return_and_risk_free_rate_preserved(self):
        import pandas as pd
        dates=pd.date_range('2024-01-01',periods=32)
        frame=pd.DataFrame({'Close':100.},index=dates)
        engine=BacktestingEngine(risk_free_rate=.07)
        metrics=engine.run_backtest({'X':pd.DataFrame({'signal':0},index=dates)},{'X':frame})
        self.assertEqual(engine.risk_free_rate,.07)
        self.assertEqual(metrics['sharpe_ratio'],0)
