#!/usr/bin/env python
#encoding: UTF-8

"""Main.py
This project is an agent-based simulation of interbank lending, to asses systemic risk. It is created in partial
fulfillment of the Capstone thesis project of the Amsterdam University College, towards the Bachelor of Science degree.
References to research in the code are cited IEEE-style, and can be found in the README.md file.
main.py is the interface used to run the simulation.
"""

__author__ = "Reinier Maat"
__date__ = "May 28, 2014"
__copyright__ = "Copyright (c) 2014, AUC Capstone Project Reinier Maat"
__license__ = "MIT"
__version__ = "0.3"
__email__ = "reinier.maat@student.auc.nl"
__status__ = "Development"

import random
import pickle
from controller import Controller
from data_collector import Experiment
from settings import *


def main():
    """
    Runs the simulation with parameters set settings.py
    :rtype : None
    """
    random.seed(RANDOM_SEED)
    simulation = Controller(import_network=False, export_network=True, build_network=True)
    pickle.dump(simulation, open(PICKLE_PATH, 'wb'))
    experiment = Experiment(asset_size=True, kappa_value=False, base_simulation_location = PICKLE_PATH)
    print('Done.')

if __name__ == '__main__':
    main()