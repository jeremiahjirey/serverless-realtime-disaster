import os
import json
import boto3
import urllib.request
from datetime import datetime
import uuid

def lambda_handler(event, context):
    url = os.getenv("BMKG_API_URL")
    stream_name = os.getenv("KINESIS_STREAM_NAME")

    # Langsung hardcode region
    kinesis = boto3.client("kinesis", region_name="us-east-1")

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        gempa = data.get("Infogempa", {}).get("gempa", {})

        if not gempa:
            print("No earthquake data found.")
            return {"status": "no_data"}

        payload = {
            "id": str(uuid.uuid4()),
            "Tanggal": gempa.get("Tanggal"),
            "Jam": gempa.get("Jam"),
            "Wilayah": gempa.get("Wilayah"),
            "Magnitude": gempa.get("Magnitude"),
            "Kedalaman": gempa.get("Kedalaman"),
            "Lintang": gempa.get("Lintang"),
            "Bujur": gempa.get("Bujur"),
            "Timestamp": datetime.utcnow().isoformat()
        }

        resp = kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(payload),
            PartitionKey="bmkg"
        )

        print("Sent to Kinesis:", resp)
        return {"status": "success", "sequence": resp["SequenceNumber"]}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}
