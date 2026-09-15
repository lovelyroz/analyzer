from typing import Dict

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
