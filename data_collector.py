"""Data_collector.py
Implements data collection and storage class.
"""


class DataCollector(object):
    """
    Collects and stores data from the simulation, for later use (e.g. by UI.py)
    """
    def __init__(self, data_file):
        self.source = data_file

