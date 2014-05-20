class BalanceSheet(object):
    """
    Implements the balance sheet of a bank.
    """
    def __init__(self, sheet_size):
        """
        All fractions are floats between 0 and 1.
        Interbank loans and borrowing are dicts in real amounts, as in {counterparty: amount}
        """
        self.assets = sheet_size
        self.liabilities = self.assets
        # Assets
        self.interbank_loans = dict()
        self.consumer_loans_fraction = 0
        self.cash_fraction = 0
        # Liabilities
        self.deposits_fraction = 0
        self.interbank_borrowing = dict()
        self.equity_fraction = 0

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

