import os
import json
import boto3
from base64 import b64decode

# Hardcode AWS region
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            payload = json.loads(b64decode(record['kinesis']['data']).decode('utf-8'))
            print("Processing record:", payload)
            table.put_item(Item=payload)
        except Exception as e:
            print("Error inserting record:", e)
    
    return {'status': 'done'}
