"""Settings.py
Sets all parameters and constants used in the simulation.
"""

# -- TIME --
STEP_SIZE = 1

# -- STATISTICS --
RANDOM_SEED = 42
PARETO_SHAPE = 0.670
PARETO_SCALE = 2994218
LOGNORMAL_MEAN = 11.910
LOGNOMRAL_STDEV = 1.078

# -- BANK NETWORK --
NUMBER_OF_BANKS_LOGNORMAL = 6300  # As in the 2014 paper by Goddard on the asset size distribution of the
NUMBER_OF_BANKS_PARETO = 180      # US banking market. [1] +/- 180 banks control 85% of all assets.
POWERLAW_PARAMETER = 3

# -- BALANCE SHEET --
DEFAULT_CONSUMER_LOANS_FRACTION = 0.5
DEFAULT_CASH_FRACTION = 0.07
DEFAULT_DEPOSITS_FRACTION = 0.70
DEFAULT_EQUITY_FRACTION = 0.075

# -- DATA --
DATA_FILE = 'path/to/data.csv'





