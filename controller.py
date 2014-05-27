"""Controller.py
Contains simulation controller class, and inherent simulation logic.
"""

import weakref
import math
import random
import networkx as nx
from statistics import Statistics
from bank import Bank
from settings import *


class Controller(object):
    """
    Controls simulation, allocation, and the underlying network.
    """
    def __init__(self):
        self.banks = []  # contains all bank objects
        self.id_to_bank = weakref.WeakValueDictionary()  # weak reference map of id's to all banks. Like pointers in C.
        self.create_banks()
        self.build_network()
        self.export_network_to_disk()
        
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
                   for degree in xrange(0, len(self.banks))]
        for i in range(0, len(degrees)):
            if degrees[i] > NUMBER_OF_BANKS:
                degrees[i] = NUMBER_OF_BANKS
        degrees.sort()
        for n in xrange(0, len(self.banks)):
            self.banks[n].out_degree = degrees[n]

    def aggregate_demand(self, borrowers_indices):
        """
        Calculates borrowing demand of borrowers referred to in the given list (references as indices of self.banks).
        :rtype: float
        """
        demand_per_bank = []
        for borrower_index in borrowers_indices:
            demand_per_bank.append(self.banks[borrower_index].borrowing_demand)
        return sum(demand_per_bank)

    def choose_borrowers(self, degree):
        """
        Chooses borrowers.
        :rtype : list
        """
        borrowers_indices = []  # refers to by index in Controller.banks
        while len(borrowers_indices) != degree:
            borrower = random.randint(0, NUMBER_OF_BANKS_LOGNORMAL + NUMBER_OF_BANKS_PARETO - 1)
            if borrower not in borrowers_indices and self.banks[borrower].borrowing_demand > 0:
                borrowers_indices.append(borrower)
        return borrowers_indices

    def make_loan(self, amount, party_id, counterparty_id):
        """
        Registers a loan with self and a counterparty.
        """
        self.id_to_bank[party_id].balance.interbank_lending[counterparty_id] = amount
        self.id_to_bank[counterparty_id].balance.interbank_borrowing[party_id] = amount

    def allocate_loans(self):
        """
        Allocates loans between banks. These form the network that holds the interbank system together.
        If supply is bigger than demand of chosen banks, higher demand banks are chosen.
        If that does not work, internal balance sheet composition is adjusted to equate supply to demand available.
        Loan size is determined in such a manner to ensure non-zero and non-trivial loans.
        :rtype : None
        """
        id_list = self.id_to_bank.keys()
        listlength = len(id_list)
        print 'Starting loan allocation...'
        for bank_id in id_list:
            # Progress indicator:
            now = id_list.index(bank_id)
            percent = 100 * (float(now) / listlength)
            print '{0}%'.format(percent)
            # ------------------
            self.banks.sort(key=lambda _bank: _bank.borrowing_demand)  # sort banks from low to to high demand
            bank = self.id_to_bank[bank_id]                           # weak reference to bank
            borrowers_indices = range(NUMBER_OF_BANKS - 1, NUMBER_OF_BANKS - int(bank.out_degree), -1)  # self.choose_borrowers(bank.out_degree)
            print borrowers_indices
            if self.aggregate_demand(borrowers_indices) < bank.lending_supply:
                 # adjust balance sheet composition:
                 borrowers_indices = [index - 1 for index in borrowers_indices]
                 old_lending_fraction = bank.lending_supply / bank.balance.assets
                 new_lending_fraction = self.aggregate_demand(borrowers_indices) / bank.balance.assets
                 addition = (old_lending_fraction - new_lending_fraction)/2
                 bank.balance.cash_fraction += addition
                 bank.balance.consumer_loans_fraction += addition
            # create interbank loans:
            for borrower_index in borrowers_indices:
                # Lend everyone fraction in accordance with demand
                counterparty = self.id_to_bank[id(self.banks[borrower_index])]  # weak ref to other bank
                loan_amount = bank.lending_supply * (counterparty.borrowing_demand /
                                                     self.aggregate_demand(borrowers_indices))
                self.make_loan(loan_amount, bank_id, id(counterparty))
            print bank.balance.interbank_lending


    def export_network_to_disk(self):
        """
        Exports network and generated data to GraphML file.
        """
        bank_network = nx.DiGraph()
        for bank in self.banks:
            bank_network.add_node(id(bank), assets=bank.balance.assets,
                                  cash=bank.balance.cash,
                                  consumer_loans=bank.balance.consumer_loans,
                                  interbank_lending=bank.balance.interbank_lending_amount,
                                  deposits=bank.balance.deposits,
                                  interbank_borrowing=bank.balance.interbank_borrowing_amount,
                                  equity=bank.balance.equity)
            for counterparty in bank.balance.interbank_lending:
                bank_network.add_edge(id(bank), counterparty, loan_amount=bank.balance.interbank_lending[counterparty])
        nx.write_gexf(bank_network, NETWORK_EXPORT_PATH + 'bank_network.gexf')
        print 'Network exported to: ' + NETWORK_EXPORT_PATH + '.'

    def test(self):
        """
        Prints asset size for all banks.
        :rtype : None
        """
        for bank in self.banks:
            bank.test()