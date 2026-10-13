"""Bounded native/Python research workflow. No order submission or latency promise."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from trading.strategies import MovingAverageCrossover
from .backtesting_engine import BacktestingEngine
from .native import signals


def load_data(csv=None, seed=7, rows=512):
    if csv:
        path = Path(csv)
        frame = pd.read_csv(path, parse_dates=["date"]).set_index("date")
        provenance = {"kind": "user_csv", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    else:
        rng = np.random.default_rng(seed)
        frame = pd.DataFrame({"Close": 100 * np.exp(np.cumsum(rng.normal(0, .01, rows)))},
                             index=pd.date_range("2024-01-01", periods=rows, freq="D"))
        provenance = {"kind": "seeded_synthetic", "seed": seed, "not_market_data": True}
    if len(frame) < 32 or not frame.index.is_monotonic_increasing or frame.index.has_duplicates:
        raise ValueError("Need at least32 unique chronological rows")
    if not np.isfinite(frame.Close).all() or (frame.Close <= 0).any():
        raise ValueError("Close values must be finite positive")
    return frame, provenance


def run(csv=None, output="artifacts", seed=7, rows=512):
    frame, provenance = load_data(csv, seed, rows)
    started = time.perf_counter()
    native = signals(frame.Close.to_numpy())
    measured_ms = (time.perf_counter() - started) * 1000
    reference = MovingAverageCrossover().generate_signals(frame).signal.shift(1).fillna(0).astype(int)
    np.testing.assert_array_equal(native, reference.to_numpy())
    engine = BacktestingEngine(initial_capital=100000, commission_per_trade=.001,
                               slippage_bps=5, max_position_size=.1)
    result = engine.run_backtest({"FIXTURE": pd.DataFrame({"signal": native}, index=frame.index)},
                                {"FIXTURE": frame})
    report = {"scope": "Causal close-to-close research simulation; no live routing or profit claim",
              "data": provenance, "rows": len(frame), "native_reference_match": True,
              "native_call_wall_ms": measured_ms,
              "latency_scope": "One local ctypes call including validation/loading; not exchange latency",
              "total_return": float(result["total_return"]), "trades": result["total_trades"],
              "commission_paid": float(result["total_commission"]), "execution_slippage_bps": 5,
              "ending_equity": float(result["final_portfolio_value"])}
    destination = Path(output); destination.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(engine.portfolio_history).assign(date=lambda f: f.date.astype(str)).to_csv(destination/"equity.csv", index=False)
    pd.DataFrame(engine.trades).to_csv(destination/"trades.csv", index=False)
    (destination/"report.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps(report, indent=2)); return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv");parser.add_argument("--output",default="artifacts")
    parser.add_argument("--rows",type=int,default=512);parser.add_argument("--seed",type=int,default=7)
    args=parser.parse_args();run(args.csv,args.output,args.seed,args.rows)

if __name__ == "__main__": main()
