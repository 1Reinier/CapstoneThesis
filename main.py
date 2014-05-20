#!/usr/bin/env python
#encoding: UTF-8

"""
This project is an agent-based simulation of interbank lending, to asses systemic risk. It is created in partial
fulfillment of the Capstone thesis project of the Amsterdam University College, towards the Bachelor of Science degree.
"""

__author__ = "Reinier Maat"
__date__ = "May 13, 2014"
__copyright__ = "Copyright (c) 2014, AUC Capstone Project Reinier Maat"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "reinier.maat@student.auc.nl"
__status__ = "Development"

from controller import Controller
from timer import TimeStepper
from data_collector import DataCollector
from UI import Interface

def main():
    """
    Runs the simulation with parameters set in the if-statement below.
    :rtype: None
    """
    clock = TimeStepper(STEPSIZE)
    simulation = Controller(NUMBEROFBANKS, POWERLAWPARAMETER)
    data = DataCollector(DATAFILE)
    plot = Interface()
    print('Done.')

if __name__ == '__main__':
    STEPSIZE = 1
    NUMBEROFBANKS = 30
    POWERLAWPARAMETER = 3
    DATAFILE = 'path/to/data.csv'
    main()