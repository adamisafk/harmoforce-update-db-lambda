import urllib3
import json

url = 'https://rpc.s0.t.hmny.io'
http = urllib3.PoolManager()

def getDelegators(validatorAddress):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "hmyv2_getDelegationsByValidator",
        "params": [validatorAddress]
    }
    headers = {'content-type': 'application/json'}
    
    response = http.request('POST', url, body = json.dumps(payload).encode('utf-8'), headers = headers)
    return json.loads(response.data)