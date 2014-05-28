"""Data_collector.py
Implements experiments, data collection and storage.
"""
import csv
import random
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
        beginning_state_banks = list(pickle.load(open(NETWORK_EXPORT_PATH + '.pickle', 'r')))
        super_simulation = Controller(True)
        id_to_bank = super_simulation.id_to_bank.copy()
        bank_id_list = id_to_bank.copy().keys()
        for bank_id in bank_id_list:
            super_simulation.banks = list(beginning_state_banks)
            for bank in super_simulation.banks:
                super_simulation.id_to_bank[bank.bank_id] = bank  # update weak ref dictionary
            bank = super_simulation.id_to_bank[bank_id]
            super_simulation.trigger(bank_id)
            fraction_failing = float(super_simulation.defaulted_banks) / float(NUMBER_OF_BANKS)
            self.asset_failure_data[bank_id] = [bank.balance.assets, fraction_failing, bank.out_degree]

    def export_data_to_csv(self, dictionary):
        with open(DATA_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key in dictionary:
                csv_writer.writerow(dictionary[key])
        print 'Data exported.'




