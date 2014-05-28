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
        beginning_state_banks = pickle.load(open(NETWORK_EXPORT_PATH + '.pickle', 'r'))
        super_simulation = Controller(True)
        id_to_bank = super_simulation.id_to_bank.copy()
        bank_id_list = id_to_bank.copy().keys()
        banks_to_fail = []
        print 'Step 1'
        for i in range(0, 150):
            n = random.randint(1, len(bank_id_list) - 1)
            banks_to_fail.append(bank_id_list[n])
            del bank_id_list[n]
        print 'Step 2'
        for bank_id in banks_to_fail:
            bank = super_simulation.id_to_bank[bank_id]
            super_simulation.trigger(bank_id)
            fraction_failing = super_simulation.defaulted_banks / NUMBER_OF_BANKS
            self.asset_failure_data[bank_id] = [bank.balance.assets, fraction_failing, bank.out_degree]
            super_simulation.banks = beginning_state_banks  # restore state

    def export_data_to_csv(self, dictionary):
        with open(DATA_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key in dictionary:
                csv_writer.writerow(dictionary[key])
        print 'Data exported.'




