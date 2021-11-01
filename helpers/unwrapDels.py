from decimal import Decimal

def harmoforce(response):
    delegatorsDict = {}
    delegations = response['Items']
    
    for delegation in delegations:
        delegatorsDict[delegation['address']]=delegation['amount']
        
    return delegatorsDict

def harmony(response):
    delegatorsDict = {}
    delegations = response['result']
    
    for delegation in delegations:
        amount = Decimal(str(delegation['amount'] * 0.000000000000000001)) # Convert Atto to ONE
        delegatorsDict[delegation['delegator_address']]=amount
        
    return delegatorsDict