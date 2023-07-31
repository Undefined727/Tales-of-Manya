import json as JSON

def load(address):
    file = open(address, 'r')
    data = JSON.load(file)
    return data