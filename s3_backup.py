import boto3
import os
from datetime import datetime

BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "stock-tracker-data-noor")
DB_PATH = "stocks.db"

def backup_database():
    """Upload the local SQLite DB to S3 as a timestamped backup."""
    s3 = boto3.client("s3")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3_key = f"backups/stocks_{timestamp}.db"
    
    try:
        s3.upload_file(DB_PATH, BUCKET_NAME, s3_key)
        s3.upload_file(DB_PATH, BUCKET_NAME, "backups/stocks_latest.db")
        print(f"Backup successful: {s3_key}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False
