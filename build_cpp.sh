#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
cmake -S cpp_engine -B cpp_engine/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp_engine/build --parallel 2
ctest --test-dir cpp_engine/build --output-on-failure
printf 'Portable causal moving-average native engine built and tested. No latency guarantees.\n'
