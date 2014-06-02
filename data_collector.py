"""Data_collector.py
Implements experiments, data collection and storage.
"""
import csv
import thread
import _multiprocessing
from controller import *


class Experiment(object):
    """
    Collects and stores data from the simulation, for later use.
    """
    def __init__(self, asset_size=True, base_simulation_location=PICKLE_PATH):
        self.asset_failure_data = {}
        print 'Starting experiment...'
        if base_simulation_location:
            self.base_simulation = pickle.load(open(base_simulation_location, 'rb'))
            self.base_bank_id_list = [bank.bank_id for bank in self.base_simulation.banks]
        if asset_size:
            self.length = len(self.base_bank_id_list)
            self.asset_size_and_default_fraction(self.base_bank_id_list)
            self.export_data_to_csv(self.asset_failure_data)

    def asset_size_and_default_fraction(self, bank_id_list):
        for bank_id in bank_id_list:
            progress = 100 * float(self.base_bank_id_list.index(bank_id)) / self.length
            print 'Asset size experiment: {0}%\r'.format(round(progress, 2)),
            simulation = copy.deepcopy(self.base_simulation)
            simulation.trigger(bank_id)
            fraction_failing = float(simulation.defaulted_banks) / float(NUMBER_OF_BANKS)
            bank = simulation.id_to_bank[bank_id]
            self.asset_failure_data[bank_id] = [bank.balance.assets, fraction_failing, bank.out_degree]
        print

    def export_data_to_csv(self, dictionary):
        with open(DATA_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key in dictionary:
                csv_writer.writerow(dictionary[key])
        print 'Data exported.'




