"""Data_collector.py
Implements experiments, data collection and storage.
"""
import csv
from settings import *
from controller import *


class Experiment(object):
    """
    Collects and stores data from the simulation, for later use.
    """
    def __init__(self):
        self.asset_failure_data = {}
        self.asset_size_and_default_fraction()
        self.export_data_to_csv(self.asset_failure_data)

    def asset_size_and_default_fraction(self):
        super_simulation = Controller()
        id_to_bank = super_simulation.id_to_bank.copy()
        for bank_id in id_to_bank:
            simulation = Controller()
            bank = simulation.id_to_bank[bank_id]
            simulation.trigger(bank_id)
            fraction_failing = simulation.defaulted_banks / NUMBER_OF_BANKS
            self.asset_failure_data[bank_id] = [bank.balance.assets, fraction_failing, bank.out_degree]

    def export_data_to_csv(self, dictionary):
        with open(DATA_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key in dictionary:
                csv_writer.writerow([key].extend(dictionary[key]))
        print 'Data exported.'




