import json
import boto3
import base64
import os

# Hardcode region
region = "us-east-1"
dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
sns = boto3.client("sns", region_name=region)

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")  

def lambda_handler(event, context):
    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        data = json.loads(payload)

        # Simpan ke DynamoDB
        table.put_item(Item=data)

        # Kirim notifikasi ke SNS
        message = (
            f"🌋 GEMPA TERDETEKSI 🌋\n\n"
            f"Wilayah: {data.get('Wilayah', '-')}\n"
            f"Magnitude: {data.get('Magnitude', '-')}\n"
            f"Koordinat: {data.get('Lintang', '-')} / {data.get('Bujur', '-')}\n"
            f"Waktu: {data.get('Tanggal', '-')} {data.get('Jam', '-')}\n"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="BMKG Gempa Terdeteksi",
            Message=message
        )

    return {"status": "ok"}
