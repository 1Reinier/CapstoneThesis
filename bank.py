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
        self.degree = math.floor(Statistics.draw_from_powerlaw(POWERLAW_EXPONENT_OUT_DEGREE, 1.0) + 0.5)

    def fail(self):
        """
        Fails the bank object. Its equity is set to 0, if it's not already so.
        Outstanding loans are redeemed.
        """
        if self.balance.equity != 0:
            self.balance.equity_fraction = 0
        #
        # redeem outstanding
        #
        pass

    @property
    def is_broke(self):
        """
        Returns boolean that is true when liabilities surpass assets. Otherwise it is false.
        :rtype : bool
        """
        if self.balance.equity <= 0:
            return True
        else:
            return False

    def borrowing_demand(self):
        """
        Returns the amount of money the bank still wants to borrow.
        """
        demand_satisfied = sum(self.balance.interbank_borrowing.values())
        return self.balance.interbank_borrowing_amount - demand_satisfied

    def lending_supply(self):
        """
        Returns the amount of money the bank is still willing to lend out.
        """
        supply_satistied = sum(self.balance.interbank_lending.values())
        return self.balance.interbank_lending_amount - supply_satistied

    def test(self):
        """
        Tests the bank class.
        :rtype : None
        """
        print self.bank_id, self.balance.assets, self.degree