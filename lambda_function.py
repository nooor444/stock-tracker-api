import urllib.request
import json
import os

EC2_URL = os.environ.get("EC2_URL", "http://YOUR_EC2_IP:8000")

def lambda_handler(event, context):
    """Triggered hourly by EventBridge — hits the /ingest endpoint on EC2."""
    try:
        url = f"{EC2_URL}/ingest"
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
        return {
            "statusCode": 200,
            "body": f"Ingestion triggered successfully: {result}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Ingestion failed: {str(e)}"
        }
