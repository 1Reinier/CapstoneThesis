import networkx as nx
from bank import Bank


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self, number_of_banks, power_law_parameter):
        self.banks = []    # contains all bank objects
        self.network = []  # placeholder for network
        self.create_banks(number_of_banks)
        self.parameter = power_law_parameter
        
    def create_banks(self, number_of_banks):
        """
        Updates self.banks.
        :rtype: None
        """
        for n in range(1, number_of_banks):
            bank = Bank()
            self.banks.append(bank)

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