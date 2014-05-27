"""Bank.py
Defines the bank class.
"""

import math
import random
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
    def capital_default(self):
        """
        Returns boolean that is true when equity reaches zero. Otherwise it is false.
        :rtype : bool
        """
        if self.balance.equity <= 0:
            return True
        else:
            return False

    @property
    def borrowing_demand(self):
        """
        Returns the amount of money the bank still wants to borrow.
        """
        demand_satisfied = sum(self.balance.interbank_borrowing.values())
        return self.balance.interbank_borrowing_amount - demand_satisfied

    @property
    def lending_supply(self):
        """
        Returns the amount of money the bank is still willing to lend out.
        """
        supply_satisfied = sum(self.balance.interbank_lending.values())
        return self.balance.interbank_lending_amount - supply_satisfied

    def lend(self, amount, counterparty):
        """
        Registers a loan with self and a counterparty.
        """
        self.balance.interbank_lending[id(counterparty)] = amount
        counterparty.balance.interbank_borrowing[id(self)] = amount

    def test(self):
        """
        Tests the bank class.
        :rtype : None
        """
        print self.bank_id, self.degree, self.balance.assets, self.balance.cash_fraction, self.balance.consumer_loans_fraction