import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL = {url}")
print(f"SUPABASE_KEY exists = {bool(key)}")
if key:
    # Print first few chars to verify without exposing secret
    print(f"SUPABASE_KEY prefix = {key[:10]}...")
