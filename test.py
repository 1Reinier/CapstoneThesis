"""Tests.py
Contains tests for the bank network simulation.
"""

from main import *


def main():
    simulation = Controller()
    simulation.test()                # prints banks' asset size, to export for statistical analysis | PASSED
#    for bank in simulation.banks:
#        bank.test()                 # prints bank_id and degree | PASSED
    pass

def check_bank(self, bank):
    if bank.bank_id in bank.balance.interbank_lending or bank.bank_id in bank.balance.interbank_borrowing:
        return False
    else:
        return True

if __name__ == "__main__":
    # test settings
    main()