import sys
import os

sys.path.append(os.path.abspath("."))

from src.etl.normalize import normalize_year, normalize_ticker

print(normalize_year("2024"))
print(normalize_ticker(" reliance "))
