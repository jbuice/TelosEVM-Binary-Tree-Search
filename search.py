import subprocess
import json

# Start and end block numbers
startBlock = 180698860
endBlock = 200000000

URL1 = "http://141.193.240.11:12000/evm"
URL2 = "http://169.197.142.4:7000/evm"

def fetchHash(blockNumber, url):
    # Convert block number to hexadecimal format
    hexBlockNumber = hex(blockNumber)

    # Use curl to make a request
    command = f'curl --data \'{{"method":"eth_getBlockByNumber","params":["{hexBlockNumber}",true],"id":292771713,"jsonrpc":"2.0"}}\' -H "Content-Type: application/json" -X POST {url} | jq'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Parse the JSON response
    response = json.loads(output)

    return response["result"]["hash"]

def binarySearchMismatch(start, end):
    if start > end:
        return None

    midBlock = (start + end) // 2

    hashA = fetchHash(midBlock, URL1)
    hashB = fetchHash(midBlock, URL2)

    if hashA != hashB:
        print(f"Mismatched hash at block {midBlock}")
        return midBlock

    # Search in the first half
    leftResult = binarySearchMismatch(start, midBlock-1)
    if leftResult:
        return leftResult

    # Search in the second half
    rightResult = binarySearchMismatch(midBlock+1, end)
    if rightResult:
        return rightResult

# Start the search
binarySearchMismatch(startBlock, endBlock)
