import json
import boto3

import helpers.harmoforceDels as harmoforceDels
import helpers.harmonyDels as harmonyDels
import helpers.unwrapDels as unwrapDels

def lambda_handler(event, context):
    # Get DB resource
    dynamodb = boto3.resource('dynamodb')
    
    # Get chosen validator
    chosenValidator = harmoforceDels.getValidator(dynamodb)
    
    # Get Harmoforce and Harmony Delegators
    harmoforceResponse = harmoforceDels.getDelegators(dynamodb)
    harmonyResponse = harmonyDels.getDelegators(chosenValidator)
    
    # Unwrap Delegators
    harmoforceDelDict = unwrapDels.harmoforce(harmoforceResponse)
    harmonyDelDict = unwrapDels.harmony(harmonyResponse)
    
    
    
    # Set delegator in DB to 0 if not present on harmony
    # TODO: handle undelegation status
    missingDels = harmoforceDelDict.keys() - harmonyDelDict.keys()
    harmoforceDels.resetDelegatorAmounts(dynamodb, missingDels)
    for missingDel in missingDels:
        harmoforceDelDict.pop(missingDel)
    # Update amount in DB if it doesn't match amount on harmony
    for harmoforceDel in harmoforceDelDict:
        harmoforceAmount = harmoforceDelDict[harmoforceDel]
        harmonyAmount = harmonyDelDict[harmoforceDel]
        if harmoforceAmount != harmonyAmount:
            harmoforceDels.updateDelegatorAmounts(dynamodb, harmoforceDel, harmonyAmount)
    
    
    return {
        'statusCode': 200,
        'body': {
            'harmoforceDels': harmoforceDelDict,
            'harmonyDels': harmonyResponse
        }
    }
