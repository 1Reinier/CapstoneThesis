class Bank(object):
    """
    Defines a bank. Balance is a dict, connections is a list of id-numbers.
    """
    def __init__(self, balance, connected_with):
        self.bank_id = id(self)                     # unique ID for each bank
        self.balance = balance                      # balance is a dict containing assets and liabilities,
                                                    # which in turn contain loans and borrowing
        self.connections = connected_with

    def trade(self):
        pass

    def new_method(self):
        pass