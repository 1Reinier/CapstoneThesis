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
        Interbank loans and borrowing are dicts in real amounts, as in {counterparty: amount}
        """
        self.assets = sheet_size
        # Assets
        self.interbank_lending = {}
        self.consumer_loans_fraction = DEFAULT_CONSUMER_LOANS_FRACTION
        self.consumer_loans = self.assets * self.consumer_loans_fraction
        self.cash_fraction = DEFAULT_CASH_FRACTION
        self.cash = self.assets * self.cash_fraction
        # Liabilities
        self.deposits_fraction = DEFAULT_DEPOSITS_FRACTION
        self.deposits = self.assets * self.deposits_fraction
        self.interbank_borrowing = {}
        self.equity_fraction = DEFAULT_EQUITY_FRACTION
        self.equity = self.assets * self.equity_fraction

    def change_cash(self, by_amount):
        self.cash += by_amount
        self.assets += by_amount
        self.cash_fraction = self.cash / self.assets
        self.equity_fraction = self.equity / self.assets

    @property
    def current_amount_of_interbank_lending(self):
        return sum(self.interbank_lending.values())

    @property
    def current_amount_of_interbank_borrowing(self):
        return sum(self.interbank_borrowing.values())

    @property
    def interbank_lending_amount_spendable(self):
        return self.assets * (1 - self.cash_fraction - self.consumer_loans_fraction)

    @property
    def interbank_borrowing_amount_demanded(self):
        return self.assets * (1 - self.deposits_fraction - self.equity_fraction)
