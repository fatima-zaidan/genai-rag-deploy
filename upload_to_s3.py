import os
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()

# AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Connect to S3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# Folder with text files
local_folder = "./data/raw"
bucket_name = "genai-rag-test-bucket"

# Upload all .txt files
for filename in os.listdir(local_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(local_folder, filename)
        s3_key = f"uploads/{filename}"  # folder inside S3
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Uploaded {filename} to s3://{bucket_name}/{s3_key}")
