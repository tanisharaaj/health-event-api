from temporal_client import get_temporal_client
from workflows.email_workflow import EmailWorkflow
import asyncio

async def main():
    client = await get_temporal_client()

    # 🟢 Construct the payload correctly
    event_payload = {
        "payload": {
            "to": "tanisha@oakmorelabs.com",
            "subject": "🚨 Health Alert: Heart Rate Spike",
            "content": (
                "Dear user123,\n\n"
                "We detected an abnormal heart rate of 140 bpm on 2025-07-14 at 11:30 AM UTC.\n"
                "Blood Pressure: 130/90\n\n"
                "Please consult a healthcare professional if this continues.\n\n"
                "— Health Monitoring System"
            )
        }
    }

    result = await client.execute_workflow(
        EmailWorkflow.run,
        event_payload,
        id="email-workflow-1",
        task_queue="health-event-task-queue",  # 🛠️ Match the worker's queue
    )

    print("🚀 Workflow result:", result)

if __name__ == "__main__":
    asyncio.run(main())
