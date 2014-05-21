"""Balance.py
Implements balance sheet class.
"""
from settings import *


class BalanceSheet(object):
    """
    Implements the balance sheet of a bank as in [2], according to empirical data from [1] and [3].
    """
    def __init__(self, sheet_size):
        """
        All fractions are floats between 0 and 1.
        Interbank loans and borrowing are dicts in real amounts, as in {counter party: amount}
        """
        self.assets = sheet_size
        self.liabilities = self.assets  # by definition
        # Assets
        self.interbank_loans = dict()
        self.consumer_loans_fraction = DEFAULT_CONSUMER_LOANS_FRACTION
        self.cash_fraction = DEFAULT_CASH_FRACTION
        # Liabilities
        self.deposits_fraction = DEFAULT_DEPOSITS_FRACTION
        self.interbank_borrowing = dict()
        self.equity_fraction = DEFAULT_EQUITY_FRACTION

    @property
    def interbank_loans_amount(self):
        return self.assets * (1 - self.cash_fraction - self.consumer_loans_fraction)

    @property
    def interbank_borrowing_amount(self):
        return self.liabilities * (1 - self.deposits_fraction - self.equity_fraction)

    @property
    def consumer_loans(self):
        return self.assets * self.consumer_loans_fraction

    @property
    def cash(self):
        return self.assets * self.cash_fraction

    @property
    def deposits(self):
        return self.liabilities * self.deposits_fraction

    @property
    def equity(self):
        return self.liabilities * self.equity_fraction

