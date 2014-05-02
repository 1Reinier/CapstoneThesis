from balance import BalanceSheet


class Bank(object):
    """
    Defines a bank. Balance is an object containing assets and liabilities,
    which in turn contain consumer loans, interbank loans, interbank borrowing, and equity.
    Interbank loans and borrowing contain a dict: {counterparty: amount}
    """
    def __init__(self):
        self.bank_id = id(self)  # unique ID for each bank
        self.balance = BalanceSheet()

    def try_borrow(self, amount, from_bank):
        """
        Returns void.
        Try and borrow the amount specified from the bank specified. If granted, this is put on the balance.
        Otherwise, nothing changes.
        """
        pass

    def review_loan(self, amount, to_bank):
        """
        Returns boolean.
        Specifies a function that governs whether to grant a loan or not.
        """
        pass

    def is_broke(self):
        """
        Returns boolean that is true when liabilities surpass assets. Otherwise it is false.
        """
        if self.balance.liabilities() > self.balance.assets():
            return True
        else:
            return False