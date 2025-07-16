from datetime import timedelta
from temporalio import workflow
from activities.send_email_activity import send_email

@workflow.defn
class EmailWorkflow:
    @workflow.run
    async def run(self, data: dict) -> str:
        workflow.logger.info(f"🚀 Running workflow with payload: {data}")
        result = await workflow.execute_activity(
            send_email,
            data,
            schedule_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✅ Activity result: {result}")
        return result
from datetime import timedelta
from temporalio import workflow
from activities.send_email_activity import send_email

@workflow.defn
class EmailWorkflow:
    @workflow.run
    async def run(self, data: dict) -> str:
        workflow.logger.info(f"🚀 Running workflow with payload: {data}")
        result = await workflow.execute_activity(
            send_email,
            data,
            schedule_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✅ Activity result: {result}")
        return result
