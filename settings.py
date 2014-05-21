"""Settings.py
Sets all parameters and constants used in the simulation.
"""

# -- TIME --
STEP_SIZE = 1

# -- STATISTICS --
RANDOM_SEED = 1
PARETO_SHAPE = 0.670
PARETO_SCALE = 2994218
LOGNORMAL_MEAN = 11.910
LOGNOMRAL_STDEV = 1.078

# -- BANK NETWORK --
NUMBER_OF_BANKS_LOGNORMAL = 6300  # As in the paper by Goddard (2014) on the asset
NUMBER_OF_BANKS_PARETO = 180      # size distribution of the US banking market.
POWERLAW_PARAMETER = 3

# -- DATA --
DATA_FILE = 'path/to/data.csv'





