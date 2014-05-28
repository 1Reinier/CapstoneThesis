"""Data_collector.py
Implements data collection and storage class.
"""


class Experiment(object):
    """
    Collects and stores data from the simulation, for later use.
    """
    def __init__(self, output_file, simulation):
        self.data_file = output_file
        self.sim = simulation

    def


