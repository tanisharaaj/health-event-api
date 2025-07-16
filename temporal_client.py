from temporalio.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

async def get_temporal_client():
    print("📬 Connecting to Temporal Cloud...")

    return await Client.connect(
        target_host=os.getenv("TEMPORAL_HOST"),
        namespace=os.getenv("TEMPORAL_NAMESPACE"),
        api_key=os.getenv("TEMPORAL_API_KEY"),  # <-- use api_key, not auth_token, headers or TLSConfig
        tls=True  # enables default TLS configuration
    )
