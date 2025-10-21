import os
import json
import boto3
from boto3.dynamodb.conditions import Key

# Hardcode AWS region
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # atau domain Amplify kamu
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(items)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
