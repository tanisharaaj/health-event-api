import os
import time
import jwt
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get JWT secret from environment
secret = os.getenv("JWT_SECRET")
if not secret:
    raise ValueError("❌ JWT_SECRET not found in environment variables.")

# Ask user for partner_id and sub
partner_id = input("Enter your partner_id: ").strip()
sub = input("Enter your client id (sub): ").strip()

# Create payload
payload = {
    "partner_id": partner_id,
    "sub": sub,
    "exp": int(time.time()) + 3600  # Token valid for 1 hour
}

# Generate token
token = jwt.encode(payload, secret, algorithm="HS256")

# Print result
print("\n✅ Generated JWT Token:\n")
print(token)
