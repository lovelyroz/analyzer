from typing import Dict

# Backward-compatible export retained for existing package consumers.
# Stage 7 V1 no longer uses hard-coded industry target P/E values; target multiples
# come from the benchmark hierarchy and versioned scenario parameters.
INDUSTRY_TARGET_PE: Dict[str, float] = {}

# V1 scenario prior. This is a versioned model parameter, not an architecture constant.
SCENARIO_WEIGHTS: Dict[str, float] = {
    "bear": 0.20,
    "base": 0.60,
    "bull": 0.20,
}

# Explicit, versioned scenario multiple parameters. These do not use Fundamental Score
# or Forecast Reliability. They remain backtestable model parameters.
SCENARIO_PE_MULTIPLIER: Dict[str, float] = {
    "bear": 0.90,
    "base": 1.00,
    "bull": 1.10,
}

MIN_INDUSTRY_PEERS = 8
MODEL_VERSION = "STAGE7_V1"
