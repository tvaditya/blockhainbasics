
MINING_REWARD = 10

open_transactions = []
owner = 'Max'
genesis_block = {
        'previous_hash': '', 
        'index': 0, 
        'transactions': []
    }
blockchain = [genesis_block]
#participants = set()
participants = {'Max'}

def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def hash_block(block):
    return "-".join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender =[[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient =[[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recieved += tx[0]            
            
    return amount_recieved - amount_sent

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def add_transaction(recipient, sender = owner,  amount = 1.0):
    transaction = { 
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender':'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    } 
    open_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_transactions
    }
    blockchain.append(block)
    return True
    #pass 

print(blockchain)

def get_user_input():
    return float(input("Transaction amount is: "))

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

#tx_amount = get_user_input()
#add_value(last_transaction=get_last_blockchain_value(), transaction_amount = tx_amount)
def get_transaction_value():
    tx_recipient = input('Enter the recipient of transaction:')
    tx_amount = float(input('Your transaction amount please? '))
    return tx_recipient, tx_amount

def print_blockchain_elements():
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)

def verify_chain():
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        return True  

waiting_for_input = True
while waiting_for_input:
    print('Please choose:')
    print('1 to add a new transaction')
    print('2 to mine the new blocks')
    print('3 to print the blockchain')
    print('4 to output participants')
    print('h to Manipulate the chain')
    print('q to Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount = amount):
            print('Transaction added!')
        else:
            print('Transaction failed!')
        print(open_transactions)
       # tx_amount  = get_transaction_value()
       # add_transaction(tx_amount, get_last_blockchain_value())
      
    elif user_choice == '2':
        mine_block()
        #print_blockchain_elements()
       # break
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {        
                'previous_hash': '', 
                'index': 0, 
                'transactions': [{'sender':'Chris','recipient':'Max','amount':101.0}]}
    elif user_choice == 'q':
        print('Quitting...')
        waiting_for_input = False
        
    else:
        print('Invalid input, please enter another choice.')
       
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain")
        break
    print(get_balance('Max'))
       
else:
    print('User left!')
    
print('Done!')  