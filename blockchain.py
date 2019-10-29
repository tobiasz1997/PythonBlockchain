# print(2+66)

blockchain = []


def add_value ():
    blockchain.append([blockchain[-1], 5.3])
    print(blockchain)


def get_last_blockchain_value () :
    """ Returns the last value of the current blockchain"""
    return blockchain[-1]


def add_value_1 (amount, last_transaction=[1]):
    """Apend a new value as well as the last blockchain value to the blockchain
    
    Arguments:
        :amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1])
    """
    blockchain.append([last_transaction, amount])
    print(blockchain)


def get_user_input():
    return float(input('your transaction amount: '))


tx_amount = get_user_input()
add_value_1(tx_amount)

tx_amount = get_user_input()
add_value_1(last_transaction=get_last_blockchain_value(),amount=tx_amount)

tx_amount = get_user_input()
add_value_1(tx_amount,get_last_blockchain_value())