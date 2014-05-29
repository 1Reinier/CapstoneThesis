"""Data_collector.py
Implements experiments, data collection and storage.
"""
import csv
import copy
from controller import *


class Experiment(object):
    """
    Collects and stores data from the simulation, for later use.
    """
    def __init__(self, asset_size=True, kappa_value=True):
        self.asset_failure_data = {}
        self.kappa_data = {}
        if asset_size:
            self.asset_size_and_default_fraction()
            self.export_data_to_csv(self.asset_failure_data)
        if kappa_value:
            pass

    def asset_size_and_default_fraction(self):
        simulation = Controller(import_network=True)
        banks_initial_state = copy.deepcopy(simulation.id_to_bank)  # safely copy init state
        bank_id_list = copy.deepcopy(banks_initial_state.keys())
        for bank_id in bank_id_list:
            simulation.banks = copy.deepcopy(banks_initial_state)
            for bank in simulation.banks:
                simulation.id_to_bank[bank.bank_id] = bank  # update weak ref dictionary
            bank = simulation.id_to_bank[bank_id]
            simulation.trigger(bank_id)
            fraction_failing = float(simulation.defaulted_banks) / float(NUMBER_OF_BANKS)
            self.asset_failure_data[bank_id] = [bank.balance.assets, fraction_failing, bank.out_degree]

    def export_data_to_csv(self, dictionary):
        with open(DATA_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for key in dictionary:
                csv_writer.writerow(dictionary[key])
        print 'Data exported.'




