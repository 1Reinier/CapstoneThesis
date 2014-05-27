"""Controller.py
Contains simulation controller class, and inherent simulation logic.
"""

import weakref
import math
from statistics import Statistics
from bank import Bank
from settings import *


class Controller(object):
    """
    Creates and keeps track of banks, and the underlying network.
    """
    def __init__(self):
        self.banks = []  # contains all bank objects
        self.id_to_bank = weakref.WeakValueDictionary()  # weak reference map of id's to all banks
        self.network = []
        self.create_banks()
        self.build_network()
        
    def create_banks(self):
        """
        Creates bank objects, stores them in self.banks, and registers them in a self.bank_to_id.
        A part of all banks follows a Pareto distribution, all others a log-normal distribution, in asset size.
        All created banks are registered in the dictionary self.id_to_bank.
        :rtype : None
        """
        for n in range(0, NUMBER_OF_BANKS_LOGNORMAL):
            bank_size = Statistics.generate_lognormal_number(LOGNORMAL_MEAN, LOGNOMRAL_STDEV)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.id_to_bank[id(bank)] = bank

        for n in range(0, NUMBER_OF_BANKS_PARETO):
            bank_size = Statistics.generate_pareto_number(PARETO_SCALE, PARETO_SHAPE)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.id_to_bank[id(bank)] = bank

    def build_network(self):
        """
        Creates the loan network between banks.
        :rtype : None

        """
        self.allocate_degrees()
        self.allocate_loans()

    def start(self, stop_before):
        """
        Starts simulation with given parameter, until no changes in variables of interest occur.
        stop_before is a parameter that sets an ultimate boundary on the simulation, in case
        variables of interest do not reach a steady state.
        :rtype : None
        """
        pass

    def allocate_degrees(self):
        """
        First sort banks by asset size, then match them with sorted degree list.
        Node degrees are governed by a power law.
        :rtype : None
        """
        self.banks.sort(key=lambda _bank: _bank.balance.assets)
        degrees = [math.floor(Statistics.draw_from_powerlaw(POWERLAW_EXPONENT_OUT_DEGREE, 1.0) + 0.5)
                   for degree in range(0, len(self.banks))]
        degrees.sort()
        for n in range(0, len(self.banks)):
            self.banks[n].degree = degrees[n]

    def allocate_loans(self):
        """
        Allocates loans between banks. This is the network that holds the interbank system together.
        """
        for bank in self.banks:
            for connection in range(0, bank.degree):
                pass

    def test(self):
        """
        Prints asset size for all banks.
        :rtype : None
        """
        self.allocate_degrees()
        for bank in self.banks:
            bank.test()