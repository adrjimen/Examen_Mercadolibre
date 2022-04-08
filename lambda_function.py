import boto3
import json
import logging
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'DNA-database'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
mutantPath = '/mutant'
statsPath = '/stats'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == statsPath:
        response = getStats()
    elif httpMethod == postMethod and path == mutantPath:
        response = saveADN(json.loads(event['body']))
    else:
        response = buildResponse(404, 'Not Found')

    return response

def getStats():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        count_human_dna = len([elem for elem in result if elem['isMutant'] == False])
        count_mutant_dna = len(result) - count_human_dna
        ratio = round(count_mutant_dna / count_human_dna, 2)
        body = {
            'count_mutant_dna': count_mutant_dna,
            'count_human_dna': count_human_dna,
            'ratio': ratio
        }
        return buildResponse(200, body)
    except:
        logger.exception('Something went wrong while scanning the database')

def saveADN(requestBody):
    try:
        response = table.scan()
        result = response['Items']
        requestBody['DNA_ID'] = len(result) + 1
        requestBody['isMutant'] = isMutant(requestBody['DNA'])
        table.put_item(Item=requestBody)
        body = {
            'Item': requestBody
        }
        if requestBody['isMutant'] == True:
            return buildResponse(200, body)
        else:
            return buildResponse(403, body)
    except:
        logger.exception('Something went wrong while checking the ADN and saving it in the database')

def buildResponse(statusCode, body):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    response['body'] = json.dumps(body)
    return response

def isMutant (dna) :
    count = 0
    n = len(dna)

    dna_matrix =[]
    for row in dna :
        row = list(row)
        dna_matrix.append(row)

    dna_mirror =[]
    for row in dna_matrix :
        row = row[::-1]
        dna_mirror.append(row)

    dna_trans = []
    for i in range(n) :
        l = []
        for j in range(n) :
            l.append(dna[j][i])
        dna_trans.append(l)

    for row in dna :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for row in dna_trans :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_matrix, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_mirror, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    return False
