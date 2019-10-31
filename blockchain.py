from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
import pickle

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Grzegorz'
participants = {'Grzegorz'}


def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            update_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(update_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(file_content[1])
        updated_transaction = []
        for tx in open_transactions:
            update_transaction = OrderedDict(
                [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
            updated_transaction.append(update_transaction)
        open_transactions = updated_transaction

    # with open('blockchain.p', mode='rb') as f:
        # file_content = pickle.loads(f.read())
        # print(file_content)
        # global blockchain
        # global open_transactions
        # blockchain = file_content['chain']
        # open_transactions = file_content['open_t']

load_data()


def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))

    # with open('blockchain.p', mode='wb') as f:
        # save_data = {
        #     'chain': blockchain,
        #     'open_t': open_transactions
        # }
        # f.write(pickle.dumps(save_data))


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                         if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_receive = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                            if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_receive - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """Apend a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender - the sender of the coins.
        :recipient - the recipient of the coins
        :amount - the amount of coins sent with the transaction (default = 1.0)
    """
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender' : 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    save_data()
    return True


def get_transaction_value():
    """Returns the input of the user as a float"""
    tx_recipient = input('Enter the sender of the transaction: ')
    tx_amount = float(input('Your transaction amount: '))
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('Output Block V')
        print(block)
    else:
        print('-' * 20)


def veryfy_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid!')
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Please choose: ')
    print('1. Add a new transaction value')
    print('2. Mine a new block')
    print('3. Output the blockchain blocks')
    print('4. Output participents')
    print('5. Check transaction validity')
    print('h => Manipulate chain')
    print('q => Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction added!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transaction ale valid')
        else:
            print('There ale invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Marek', 'recipient': 'Grzegorz', 'amount': 200.0}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid')
    if not veryfy_chain():
        print_blockchain_elements()
        print('invalid blockchain!!!')
        break
    print('^^^^^^^^^^^^')
    print('Balance of {}: {:6.2f}'.format('Grzegorz', get_balance('Grzegorz')))
else:
    print('User left!')

print('Thank you!')
