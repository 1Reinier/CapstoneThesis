import networkx as nx
import weakref
from statistics import Statistics
from bank import Bank
from settings import *


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self):
        self.banks = [] # contains all bank objects
        self.bank_to_id = weakref.WeakValueDictionary()  # reference map to all banks
        self.network = []  # placeholder for network
        self.create_banks(NUMBER_OF_BANKS_LOGNORMAL, NUMBER_OF_BANKS_PARETO)
        
    def create_banks(self, number_of_banks_lognormal, number_of_banks_pareto):
        """
        Creates bank objects, stores them in self.banks, and registers them in a WeakRefDict.
        :rtype: None
        """
        for n in range(0, number_of_banks_lognormal):
            bank_size = Statistics.generate_lognormal_number(LOGNORMAL_MEAN, LOGNOMRAL_STDEV)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.bank_to_id[id(bank)] = bank
        for n in range(0, number_of_banks_pareto):
            bank_size = Statistics.generate_pareto_number(PARETO_SCALE, PARETO_SHAPE)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.bank_to_id[id(bank)] = bank

    def build_network(self, number_of_banks):
        """
        Creates a network of banks with a chosen amount.
        :rtype: None

        """
        self.network = nx.generators.random_graphs.barabasi_albert_graph(number_of_banks, 3)

    def start(self, stop_before):
        """
        Starts simulation with given parameter, until no changes in variables of interest occur.
        stop_before is a parameter that sets an ultimate boundary on the simulation, in case
        variables of interest do not reach a steady state.
        :rtype: None
        """
        pass