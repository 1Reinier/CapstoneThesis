"""Bank.py
Defines the bank class.
"""

import math
from balance import BalanceSheet
from settings import *
from statistics import Statistics


class Bank(object):
    """
    Defines a bank.
    bank_size specifies the balance sheet size of the bank in dollars.
    """
    def __init__(self, bank_size):
        self.bank_id = id(self)  # unique id for each bank object (= memory address)
        self.balance = BalanceSheet(bank_size)
        self.out_degree = math.floor(Statistics.draw_from_powerlaw(POWERLAW_EXPONENT_OUT_DEGREE, 1.0) + 0.5)
        self.in_default = False

    @property
    def borrowing_demand(self):
        """
        Returns the amount of money the bank still wants to borrow.
        """
        demand_satisfied = sum(self.balance.interbank_borrowing.values())
        return self.balance.interbank_borrowing_amount_demanded - demand_satisfied

    @property
    def lending_supply(self):
        """
        Returns the amount of money the bank is still willing to lend out.
        """
        supply_satisfied = sum(self.balance.interbank_lending.values())
        return self.balance.interbank_lending_amount_spendable - supply_satisfied

    def test(self):
        """
        Tests the bank class.
        :rtype : None
        """
        print self.bank_id, self.out_degree, self.balance.assets, \
            self.balance.cash_fraction, self.balance.consumer_loans_fraction