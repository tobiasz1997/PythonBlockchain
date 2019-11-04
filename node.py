from uuid import uuid4

from blockchain import Blockchain
from varification import Verification


class Node:
    def __init__(self):
        #self.id = str(uuid4())
        self.id = 'Grzegorz'
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """Returns the input of the user as a float"""
        tx_recipient = input('Enter the sender of the transaction: ')
        tx_amount = float(input('Your transaction amount: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print('Output Block V')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please choose: ')
            print('1. Add a new transaction value')
            print('2. Mine a new block')
            print('3. Output the blockchain blocks')
            print('4. Check transaction validity')
            # print('h => Manipulate chain')
            print('q => Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print('Transaction added!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transaction ale valid')
                else:
                    print('There ale invalid transactions')
            # elif user_choice == 'h':
            #     if len(blockchain) >= 1:
            #         blockchain[0] = {
            #             'previous_hash': '',
            #             'index': 0,
            #             'transactions': [{'sender': 'Marek', 'recipient': 'Grzegorz', 'amount': 100.0}]
            #         }
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid')
            if not Verification.veryfy_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('invalid blockchain!!!')
                break
            print('^^^^^^^^^^^^')
            print('Balance of {}: {:6.2f}'.format(
                self.id, self.blockchain.get_balance()))
        else:
            print('User left!')

        print('Thank you!')


node = Node()
node.listen_for_input()
