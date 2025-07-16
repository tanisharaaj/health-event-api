import os
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.email_workflow import EmailWorkflow
from activities.send_email_activity import send_email
from temporal_client import get_temporal_client

async def main():
    client = await get_temporal_client()

    worker = Worker(
        client,
        task_queue="health-event-task-queue",
        workflows=[EmailWorkflow],
        activities=[send_email],
    )

    print("✅ Email worker started. Polling for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
