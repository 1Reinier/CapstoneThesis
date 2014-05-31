"""Controller.py
Contains simulation controller class, and inherent simulation logic.
"""

import copy
import math
import networkx as nx
import pickle
from statistics import Statistics
from bank import Bank
from settings import *


class Controller(object):
    """
    Controls simulation, allocation, and the underlying network.
    """
    def __init__(self, import_network=False, export_network=False, build_network=False):
        self.banks = []  # contains all bank objects
        self.id_to_bank = dict()  # reference map of id's to all banks.
        if build_network:
            self.build_network()
        if export_network:
            self.export_network_to_disk(NETWORK_EXPORT_PATH)
        if import_network:
            self.import_network_from_disk(NETWORK_EXPORT_PATH)  # imports network created earlier by the program
        self.defaulted_banks = 0.0
        #self.trigger(self.banks[50].bank_id) # initial trigger (example)
        #self.export_network_to_disk(FAILED_NETWORK_EXPORT_PATH)  # save network after triggering defaults.
        
    def build_network(self):
        """
        Creates the loan network between banks.
        :rtype : None

        """
        self.create_banks()
        self.allocate_degrees()
        self.allocate_loans()

    def create_banks(self):
        """
        Creates bank objects, stores them in self.banks, and registers them in a self.bank_to_id.
        A part of all banks follows a Pareto distribution, all others a log-normal distribution, in asset size.
        All created banks are registered in the dictionary self.id_to_bank.
        :rtype : None
        """
        for n in xrange(0, NUMBER_OF_BANKS_LOGNORMAL):
            bank_size = Statistics.generate_lognormal_number(LOGNORMAL_MEAN, LOGNOMRAL_STDEV)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.id_to_bank[id(bank)] = bank

        for n in xrange(0, NUMBER_OF_BANKS_PARETO):
            bank_size = Statistics.generate_pareto_number(PARETO_SCALE, PARETO_SHAPE)
            bank = Bank(bank_size)
            self.banks.append(bank)
            self.id_to_bank[id(bank)] = bank

    def allocate_degrees(self):
        """
        First sort banks by asset size, then match them with sorted degree list.
        Node degrees are governed by a power law.
        :rtype : None
        """
        self.banks.sort(key=lambda _bank: _bank.balance.assets)
        degrees = [math.floor(Statistics.draw_from_powerlaw(POWERLAW_EXPONENT_OUT_DEGREE, 1.0) + 0.6748)
                   for degree in xrange(0, len(self.banks))]
        for i in xrange(0, len(degrees)):
            if degrees[i] > MAX_K_OUT:
                degrees[i] = MAX_K_OUT
        degrees.sort()
        for n in xrange(0, len(self.banks)):
            self.banks[n].out_degree = degrees[n]

    def allocate_loans(self):
        """
        Allocates loans between banks. These form the network that holds the interbank system together.
        If supply is bigger than demand of chosen banks, higher demand banks are chosen.
        If that does not work, internal balance sheet composition is adjusted to equate supply to demand available.
        Loan size is determined in such a manner to ensure non-zero and non-trivial loans.
        :rtype : None
        """
        id_list = copy.deepcopy(self.id_to_bank.keys())
        length = len(id_list)
        print 'Starting loan allocation...'

        for bank_id in id_list:
            # Progress indicator:
            progress = 100 * (float(id_list.index(bank_id)) / length)
            print 'Loan allocation: {0}%\r'.format(round(progress, 2)),

            # allocation of bank-bank connections:
            self.banks.sort(key=lambda _bank: _bank.borrowing_demand)  # sort banks from low to to high demand
            bank = self.id_to_bank[bank_id]                            # reference to bank
            borrowers_indices = range(NUMBER_OF_BANKS - 1, NUMBER_OF_BANKS - int(bank.out_degree) - 1, -1)
            borrowers_ids = [self.banks[index].bank_id for index in borrowers_indices]
            if bank_id in borrowers_ids:
                # no loans to self
                place = borrowers_ids.index(bank_id)
                borrowers_ids[place] = self.banks[NUMBER_OF_BANKS - int(bank.out_degree) - 2].bank_id

            if self.aggregate_demand(borrowers_ids) < bank.lending_supply:
                 # adjust balance sheet composition:
                 old_lending_fraction = bank.lending_supply / bank.balance.assets
                 new_lending_fraction = self.aggregate_demand(borrowers_ids) / bank.balance.assets
                 addition = (old_lending_fraction - new_lending_fraction) / 2
                 bank.balance.cash_fraction += addition
                 bank.balance.consumer_loans_fraction += addition

            # create interbank loans:
            for borrower_id in borrowers_ids:

                # Lend everyone fraction in accordance with demand
                counterparty_id = borrower_id
                if bank_id == counterparty_id:
                    raise AssertionError
                counterparty = self.id_to_bank[counterparty_id]  # ref to other bank
                loan_amount = bank.lending_supply*(counterparty.borrowing_demand / self.aggregate_demand(borrowers_ids))
                self.make_loan(loan_amount, bank_id, counterparty_id)
        print

    def aggregate_demand(self, borrowers_ids):
        """
        Calculates borrowing demand of borrowers referred to in the given list (references as indices of self.banks).
        :rtype: float
        """
        demand_per_bank = []
        for borrower_id in borrowers_ids:
            demand_per_bank.append(self.id_to_bank[borrower_id].borrowing_demand)
        return sum(demand_per_bank)

    def make_loan(self, amount, party_id, counterparty_id):
        """
        Registers a loan with self and a counterparty.
        """
        self.id_to_bank[party_id].balance.interbank_lending[counterparty_id] = amount
        self.id_to_bank[counterparty_id].balance.interbank_borrowing[party_id] = amount


    def trigger(self, bank_id, consumer_loan_recovery_fraction=COMMON_RECOVERY_PARAMETER):
        """
        Initial default trigger.
        """
        bank = self.id_to_bank[bank_id]
        loss = bank.balance.equity
        bank.balance.equity = 0.0
        bank.balance.cash -= loss
        self.go_into_default(bank_id, consumer_loan_recovery_fraction)

    def go_into_default(self, bank_id, consumer_loan_recovery_fraction=COMMON_RECOVERY_PARAMETER):
        """
        Fails the bank object.
        Triggers contagion mechanism.
        """
        bank = self.id_to_bank[bank_id]
        if not(bank.in_default):
            bank.in_default = True
            # keeping score:
            self.defaulted_banks += 1.0

            # Workaround for bug:
            interbank_lending_backup = copy.deepcopy(bank.balance.interbank_lending)
            interbank_borrowing_backup = copy.deepcopy(bank.balance.interbank_borrowing)

            # redeem outstanding loans:
            retrievable = 0
            for counterparty_id in interbank_lending_backup:
                counterparty = self.id_to_bank[counterparty_id]
                if bank.balance.interbank_lending[counterparty_id] >= counterparty.balance.cash:
                    retrievable = counterparty.balance.cash
                    counterparty.balance.cash = 0.0
                else:
                    retrievable = bank.balance.interbank_lending[counterparty_id]
                    counterparty.balance.cash -= retrievable
                counterparty.balance.interbank_borrowing[bank.bank_id] = 0
                bank.balance.interbank_lending[counterparty_id] = 0
            money_retrieved = (consumer_loan_recovery_fraction * bank.balance.consumer_loans) + retrievable
            money_left = money_retrieved + bank.balance.cash - bank.balance.deposits
            if money_left > 0:
                bank.balance.cash = money_left
            else:
                bank.balance.cash = 0.0
            bank.balance.deposits = 0.0

            # default on borrowed money. If money is left after depositors pay-out, creditors are paid:
            if bank.balance.cash > 0.0:
                return_fraction = 0
                if bank.balance.current_amount_of_interbank_borrowing != 0:
                    # fraction repaid:
                    return_fraction = bank.balance.cash / bank.balance.current_amount_of_interbank_borrowing
                if return_fraction > 1.0:
                    return_fraction = 1.0
                for counterparty_id in interbank_borrowing_backup:
                    loan_size = bank.balance.interbank_borrowing[counterparty_id]
                    counterparty = self.id_to_bank[counterparty_id]
                    loss = (1.0 - return_fraction) * loan_size
                    if loss < counterparty.balance.equity:
                        counterparty.balance.equity -= loss
                    else:
                        counterparty.balance.equity = 0.0
                    del counterparty.balance.interbank_lending[bank.bank_id]
                    del bank.balance.interbank_borrowing[counterparty_id]
            else:
                # default on borrowed money without money left:
                for counterparty_id in interbank_borrowing_backup:
                    loss = bank.balance.interbank_borrowing[counterparty_id]
                    counterparty = self.id_to_bank[counterparty_id]
                    if loss < counterparty.balance.equity:
                        counterparty.balance.equity -= loss
                    else:
                        counterparty.balance.equity = 0.0
                    del counterparty.balance.interbank_lending[bank.bank_id]
                    del bank.balance.interbank_borrowing[counterparty_id]

            # check for, and trigger next defaults, if they occur:
            for counterparty_id in interbank_borrowing_backup:
                counterparty = self.id_to_bank[counterparty_id]
                if counterparty.balance.equity <= 0.0:
                    self.go_into_default(counterparty_id)
            for counterparty_id in interbank_lending_backup:
                counterparty = self.id_to_bank[counterparty_id]
                if counterparty.balance.cash <= 0.0:
                    self.go_into_default(counterparty_id)

    def export_network_to_disk(self, path):
        """
        Exports network and generated data to GraphML file and as a pickle.
        """
        bank_network = nx.DiGraph()
        for bank in self.banks:
            bank_network.add_node(bank.bank_id, assets=bank.balance.assets,
                                  cash=bank.balance.cash,
                                  consumer_loans=bank.balance.consumer_loans,
                                  interbank_lending=bank.balance.current_amount_of_interbank_lending,
                                  deposits=bank.balance.deposits,
                                  interbank_borrowing=bank.balance.current_amount_of_interbank_borrowing,
                                  equity=bank.balance.equity)
            for counterparty in bank.balance.interbank_lending:
                bank_network.add_edge(bank.bank_id, counterparty, loan_amount=bank.balance.interbank_lending[counterparty])
        # save GEXF:
        nx.write_gexf(bank_network, path + '.gexf')
        print 'Network exported to: ' + NETWORK_EXPORT_PATH + '.'

    def import_state_from_disk(self, path):
        """
        Imports network from pickle on disk and stores it in self.banks.
        """
        self.banks = pickle.load(open(path + '.pickle', 'r'))
        for bank in self.banks:
            self.id_to_bank[bank.bank_id] = bank  # update weak ref dictionary
        print 'Network import from disk: done.'

    def test(self):
        """
        Prints various bank properties.
        :rtype : None
        """
        for bank in self.banks:
            bank.test()

    def check_bank(self, bank):
        if bank.bank_id in bank.balance.interbank_lending or bank.bank_id in bank.balance.interbank_borrowing:
            return False
        else:
            return True