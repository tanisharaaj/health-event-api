import requests
import jwt
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the secret key from the environment
JWT_SECRET = os.getenv("JWT_SECRET")

# Generate JWT token
token = jwt.encode({"user": "tester"}, JWT_SECRET, algorithm="HS256")

# Create request headers
headers = {
    "Authorization": f"Bearer {token}"
}

# Define payload
payload = {
    "to_email": os.getenv("EMAIL_TO"),
    "subject": "🧪 Testing Email Trigger from FastAPI",
    "content": "✅ This email was sent via the /send-event API using Temporal!"
}

# Send request to FastAPI endpoint
response = requests.post("http://localhost:8000/send-event", json=payload, headers=headers)

# Print result
print("Status code:", response.status_code)
print("Response:", response.json())

