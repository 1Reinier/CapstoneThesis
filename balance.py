class BalanceSheet(object):
    """
    Implements the balance sheet of a bank.
    """
    def __init__(self):
        # Assets
        self.interbank_loans = dict()
        self.consumer_loans = dict()
        self.cash = 0
        # Liabilities
        self.deposits = 0
        self.interbank_borrowing = dict()
        self.equity = 0

    def assets(self):
        """
        Returns a float of all assets.
        :rtype: float
        """
        return sum(self.interbank_loans.values()) + sum(self.consumer_loans.values()) + self.cash

    def liabilities(self):
        """
        Returns a float of all liabilities.
        :rtype: float
        """
        return self.deposits + sum(self.interbank_borrowing.values()) + self.equity