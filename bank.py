"""Bank.py
Defines the bank class.
"""

from balance import BalanceSheet


class Bank(object):
    """
    Defines a bank.
    bank_size specifies the balance sheet size of the bank in dollars.
    """
    def __init__(self, bank_size):
        self.bank_id = id(self)  # unique ID for each bank
        self.balance = BalanceSheet(bank_size)

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
        :rtype : void
        """
        pass

    def review_loan(self, amount, to_bank):
        """
        Specifies a function that governs whether to grant a loan or not.
        :rtype : bool
        """
        pass