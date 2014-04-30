import networkx as nx


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self):
        self.registry = []  # contains all bank IDs

    def create_network(self, number_of_banks, network_style):
        """
        Creates a network of banks with a chosen amount, and a style parameter (dict), containing a valid NetworkX
        function name as key (such as nx.barabasi_albert_graph), and the required parameter as value.

        """
        network_style[0](number_of_banks)