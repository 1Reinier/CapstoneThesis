import networkx as nx
import weakref
import statistics
from bank import Bank


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self, number_of_banks, powerlawparameter, paretoscale, paretoshape, lognormalmu, lognormalsigma):
        self.banks = [] # contains all bank objects
        self.bank_to_id = weakref.WeakValueDictionary()  # reference map to all banks
        self.network = []  # placeholder for network
        self.create_banks(number_of_banks)
        self.power_law_parameter = powerlawparameter
        self.pareto_shape = paretoshape
        self.pareto_scale = paretoscale
        self.lognormal_mean = lognormalmu
        self.lognormal_stdev = lognormalsigma
        
    def create_banks(self, number_of_banks):
        """
        Creates bank objects, stores them in self.banks, and registers them in a WeakRefDict.
        :rtype: None
        """
        for n in range(1, number_of_banks - 180):
            bank_size = 0
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