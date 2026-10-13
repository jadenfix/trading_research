"""ctypes integration for the actually built portable C++ research core."""
import ctypes
from pathlib import Path
import numpy as np


def signals(prices, fast=5, slow=20, library=None):
    prices = np.ascontiguousarray(prices, dtype=np.float64)
    if prices.ndim != 1:
        raise ValueError("Prices must be one dimensional")
    if not isinstance(fast, int) or not isinstance(slow, int) or fast < 1 or slow <= fast:
        raise ValueError("Require 0 < fast < slow")
    root = Path(__file__).resolve().parents[1]
    path = Path(library) if library else root / "cpp_engine/build/libresearch_native.so"
    if not path.is_file():
        raise RuntimeError("Native library absent; run bash build_cpp.sh first")
    lib = ctypes.CDLL(str(path.resolve()))
    func = lib.research_ma
    func.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_size_t,
                     ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_int)]
    func.restype = ctypes.c_int
    output = np.zeros(len(prices), dtype=np.int32)
    if func(prices.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), len(prices),
            fast, slow, output.ctypes.data_as(ctypes.POINTER(ctypes.c_int))):
        raise ValueError("Prices must be finite positive and longer than slow window")
    return output
