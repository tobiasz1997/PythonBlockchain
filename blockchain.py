# print(2+66)

blockchain = []


def add_value():
    blockchain.append([blockchain[-1], 5.3])
    print(blockchain)


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(amount, last_transaction=[1]):
    """Apend a new value as well as the last blockchain value to the blockchain

    Arguments:
        :amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, amount])


def get_transaction_value():
    """Returns the input of the user as a float"""
    return float(input('your transaction amount: '))


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('output Block')
        print(block)
    else:
        print('-' * 20)


def veryfy_chain():
    #block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        if blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     if block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index +=1
    return is_valid


# tx_amount = get_transaction_value()
# add_transaction(tx_amount)

# tx_amount = get_transaction_value()
# add_transaction(last_transaction=get_last_blockchain_value(),amount=tx_amount)

# tx_amount = get_transaction_value()
# add_transaction(tx_amount,get_last_blockchain_value())

waiting_for_input = True

while waiting_for_input:
    print('Please choose: ')
    print('1. Add a new transaction value')
    print('2. Output the blockchain blocks')
    print('h => Manipulate chain')
    print('q => Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >=1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid')
    if not veryfy_chain():
        print_blockchain_elements()
        print('invalid blockchain!!!')
        break
else:
    print('User left!')

print('Thank you!')
