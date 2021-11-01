import boto3
from boto3.dynamodb.conditions import Key
import json

def getDelegators(dynamodb):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('harmoforce_delegators')
    scan_kwargs = {
        'ProjectionExpression': "address, amount, isValidator",
        'FilterExpression': Key('isValidator').eq(1 == 0),
    }

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
        
    return response
    
def resetDelegatorAmounts(dynamodb, delegators):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('harmoforce_delegators')
    
    for delegator in delegators:
        response = table.update_item(
            Key={
                'address': delegator
            },
            UpdateExpression="set amount=:a",
            ExpressionAttributeValues={
                ':a': 0
            },
            ReturnValues="UPDATED_NEW"
        )
        
def updateDelegatorAmounts(dynamodb, delegator, amount):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('harmoforce_delegators')
    
    response = table.update_item(
        Key={
            'address': delegator
        },
        UpdateExpression="set amount=:a",
        ExpressionAttributeValues={
            ':a': amount
        },
        ReturnValues="UPDATED_NEW"
    )
    
def getValidator(dynamodb):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('harmoforce_delegators')
    scan_kwargs = {
        'ProjectionExpression': "address, amount, isValidator",
        'FilterExpression': Key('isValidator').eq(0 == 0),
    }
    
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
        
    return response['Items'][0]['address']