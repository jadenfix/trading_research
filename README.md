# Trading research

A reproducible research workbench joining a portable C++ moving-average core to Python strategy validation and cost-aware portfolio accounting.

## Run the complete research lane

```bash
python -m pip install -r requirements-research.txt
bash build_cpp.sh
python -m unittest discover -s tests -v
python -m research.workbench --rows 512 --output artifacts
```

The default data are **seeded synthetic observations**, visibly identified in `report.json`. Supply `--csv your_prices.csv` for your data: columns `date,Close`, at least32 finite positive prices, unique chronological dates. The input hash is recorded. Outputs include equity and trade CSVs and a JSON receipt.

The native core computes positions at time t from prices through t−1. Every execution checks its complete signal vector against the existing Python moving-average strategy shifted by one bar. The backtest uses10% position limits,10bps commission and5bps execution slippage; slippage is charged once. Positions are marked to market, and ending positions remain open in final equity. Borrow fees, liquidity limits and an exchange router are outside this workflow.

## Native scope

The CMake default builds `libresearch_native` and a real input/causality test without Boost, pybind11, GPU or AVX requirements. `research.native` loads that actual library through ctypes and raises if it is absent. Local call timing includes library loading and validation and is **not exchange latency**. No nanosecond, throughput or profitability guarantee is made.

Earlier C++ risk/order/DPDK/binding sketches remain in the source tree. Their manifest referenced absent files and is preserved as `cpp_engine/CMakeLists.experimental.txt`; those components are not part of the working lane. Rust and Go prototypes remain separately available, with their own unfinished interfaces. Historical report JSONs are archival examples, not current measured proof. Python market fetching lazily imports optional `yfinance`; this workflow makes no network call or submits any order.
