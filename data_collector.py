"""Data_collector.py
Implements data collection and storage class.
"""


class Experiment(object):
    """
    Collects and stores data from the simulation, for later use (e.g. by UI.py)
    """
    def __init__(self, output_file):
        self.data_file = output_file


