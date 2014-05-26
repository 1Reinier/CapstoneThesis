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
        self.degree = math.floor(Statistics.draw_from_powerlaw(POWERLAW_EXPONENT_OUT_DEGREE, 1.0))

    def fail(self):
        """
        Fails the bank object. Triggers Its equity is set to 0, if it's not already so.
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

    def try_borrow(self, amount, from_bank):
        """
        Try and borrow the amount specified from the bank specified. If granted, this is put on the balance.
        Otherwise, nothing changes.
        :rtype : None
        """
        pass

    def review_loan(self, amount, to_bank):
        """
        Specifies a function that governs whether to grant a loan or not.
        :rtype : bool
        """
        pass

    def test(self):
        """
        Tests the bank class.
        :rtype : None
        """
        print self.bank_id, self.degree