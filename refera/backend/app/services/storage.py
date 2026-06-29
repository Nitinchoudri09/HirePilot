import os
import uuid
from typing import Optional
from app.config import get_settings

settings = get_settings()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_file(content: bytes, filename: str, user_id: int) -> str:
    ext = os.path.splitext(filename)[1]
    unique_name = f"{user_id}_{uuid.uuid4().hex}{ext}"
    local_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(local_path, "wb") as f:
        f.write(content)

    if settings.AWS_S3_BUCKET and settings.AWS_ACCESS_KEY_ID:
        try:
            import boto3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            key = f"resumes/{unique_name}"
            s3.put_object(Bucket=settings.AWS_S3_BUCKET, Key=key, Body=content)
            return f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
        except Exception:
            pass

    return f"/uploads/{unique_name}"
