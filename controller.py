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
    Controls simulation, allocation, and the underlying network.
    """
    def __init__(self):
        self.banks = []  # contains all bank objects
        self.id_to_bank = weakref.WeakValueDictionary()  # weak reference map of id's to all banks. Like pointers in C.
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
                   for degree in xrange(0, len(self.banks))]
        degrees.sort()
        for n in xrange(0, len(self.banks)):
            self.banks[n].degree = degrees[n]

    def aggregate_demand(self, borrowers_indices):
        """
        Calculates borrowing demand of borrowers referred to in the given list (references as indices of self.banks).
        :rtype: float
        """
        demand_per_bank =[]
        for borrower_index in borrowers_indices:
            demand_per_bank.append(self.banks[borrower_index].borrowing_demand)
        return sum(demand_per_bank)

    def allocate_loans(self):
        """
        Allocates loans between banks. These form the network that holds the interbank system together.
        If supply is bigger than demand of chosen banks, higher demand banks are chosen.
        If that does not work, internal balance sheet composition is adjusted to equate supply to demand available.
        Loan size is determined in such a manner to ensure non-zero and non-trivial loans.
        :rtype : None
        """
        id_list = self.id_to_bank.keys()
        total = len(id_list)
        for bank_id in self.id_to_bank:
            now = id_list.index(bank_id)
            percent = 100*(float(now)/total)
            print '{0}%'.format(percent)
            self.banks.sort(key=lambda _bank: _bank.borrowing_demand)  # sort banks from low to to high demand
            bank = self.id_to_bank[bank_id]                           # weak reference to bank
            borrowers_indices = bank.choose_borrowers()
            try:
                while self.aggregate_demand(borrowers_indices) < bank.lending_supply:
                    borrowers_indices = [index + 1 for index in borrowers_indices]  # find higher demand banks
            except IndexError:
                # adjust balance sheet composition:
                borrowers_indices = [index - 1 for index in borrowers_indices]  # go back to working index
                old_lending_fraction = bank.lending_supply / bank.balance.assets
                new_lending_fraction = self.aggregate_demand(borrowers_indices) / bank.balance.assets
                addition = (old_lending_fraction - new_lending_fraction)/2
                bank.balance.cash_fraction += addition
                bank.balance.consumer_loan_fraction += addition
            # create interbank loans:
            borrowers_indices.sort()
            for borrowers_index in borrowers_indices:
                # Lend everyone fraction in accordance with demand
                counterparty = self.id_to_bank[id(self.banks[borrowers_index])]  # weak ref to other bank
                loan_amount = bank.lending_supply * (counterparty.borrowing_demand /
                                                     self.aggregate_demand(borrowers_indices))
                bank.lend(loan_amount, counterparty)

    def test(self):
        """
        Prints asset size for all banks.
        :rtype : None
        """
        for bank in self.banks:
            bank.test()