import networkx as nx


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self):
        self.banks = []    # contains all bank objects
        self.network = []  # placeholder for network
        
    def create_banks(self, number_of_banks):
        """
        Returns void.
        Updates self.banks
        """
        
        pass

    def build_network(self, number_of_banks, network_style):
        """
        Returns void.
        Creates a network of banks with a chosen amount, and a style parameter (dict), containing a valid NetworkX
        function name as key (such as nx.barabasi_albert_graph), and the required parameter as value.

        """
        self.network = network_style[0](number_of_banks)

    def start(self, stop_before):
        """
        Returns void.
        Starts simulation with given parameter, until no changes in variables of interest occur.
        stop_before is a parameter that sets an ultimate boundary on the simulation, in case
        variables of interest do not reach a steady state.
        """
        pass