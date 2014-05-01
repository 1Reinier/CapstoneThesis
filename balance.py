class BalanceSheet(object):
    '''
    Implements the balance sheet of a bank.
    '''
    def __init__(self):
        # Assets
        self.interbank_loans = dict()
        self.consumer_loans = dict()
        # Liabilities
        self.interbank_borrowing = dict()
        self.equity = 0  # int or float

    def assets(self):
        '''
        Returns an int or float of all assets.
        '''
        return sum(self.interbank_loans.values()) + sum(self.consumer_loans.values())

    def liabilities(self):
        '''
        Returns an int or float of all liabilities.
        '''
        return sum(self.interbank_borrowing.values()) + self.equity