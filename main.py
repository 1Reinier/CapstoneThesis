#!/usr/bin/env python
#encoding: UTF-8

"""Main.py
This project is an agent-based simulation of interbank lending, to asses systemic risk. It is created in partial
fulfillment of the Capstone thesis project of the Amsterdam University College, towards the Bachelor of Science degree.

References to research in the code are cited IEEE-style, and can be found in the README.md file.

main.py is the interface used to run the simulation.
"""

__author__ = "Reinier Maat"
__date__ = "May 25, 2014"
__copyright__ = "Copyright (c) 2014, AUC Capstone Project Reinier Maat"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "reinier.maat@student.auc.nl"
__status__ = "Development"

import random
from controller import Controller
from timer import TimeStepper
from data_collector import DataCollector
from UI import Interface
from settings import *


def main():
    """
    Runs the simulation with parameters set settings.py
    :rtype: None
    """
    random.seed(RANDOM_SEED)
    clock = TimeStepper(STEP_SIZE)
    simulation = Controller()
    data = DataCollector(DATA_FILE)
    plot = Interface()
    print('Done.')

if __name__ == '__main__':
    main()