from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import jwt
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from fastapi import Body
from temporal_client import get_temporal_client
from workflows.email_workflow import EmailWorkflow
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Health Event API",
    description="API to trigger health event workflows securely.",
    version="1.0.0"
)

# JWT Auth scheme
security = HTTPBearer()

# ✅ Nested model for payload
class PayloadModel(BaseModel):
    to: str
    subject: Optional[str] = "No subject"
    content: Optional[str] = ""

# ✅ Main input schema
class EventCaptureRequest(BaseModel):
    event_code: str
    partner_id: str
    user_id: str
    timestamp: datetime
    payload: PayloadModel


@app.get("/")
def read_root():
    return {"message": "Health Event API is running."}


@app.post("/api/events/capture")
async def send_event(
    event: EventCaptureRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    secret = os.getenv("JWT_SECRET")

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_partner_id = payload.get("partner_id")
    token_sub = payload.get("sub")

    if not token_partner_id or not token_sub:
        raise HTTPException(status_code=403, detail="Token missing required claims: 'partner_id' and/or 'sub'")

    if token_partner_id != event.partner_id:
        raise HTTPException(
            status_code=403,
            detail=f"partner_id mismatch: token({token_partner_id}) != body({event.partner_id})"
        )

    # ✅ TIMESTAMP FORMAT AND FRESHNESS VALIDATION
    try:
        event_time = event.timestamp
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format. Must be ISO 8601.")

    now = datetime.now(timezone.utc)

    if abs(now - event_time) > timedelta(minutes=5):
        raise HTTPException(status_code=400, detail="Timestamp is outside the allowed ±5 minute window.")

    # ✅ START TEMPORAL WORKFLOW
    client = await get_temporal_client()
    handle = await client.start_workflow(
        EmailWorkflow.run,
        event.dict(),  # Pass the full event as a dict
        id=f"health-event-{int(time.time())}",
        task_queue="health-event-task-queue"
    )

    # ✅ SUCCESS RESPONSE PER SPEC
    return {
        "status": "success",
        "event_code": event.event_code,
        "received_at": now.isoformat() + "Z"
    }




@app.post("/api/events/appointment-cancelled")
async def appointment_cancelled(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/appointment-scheduled")
async def appointment_scheduled(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/consult-request-approved")
async def consult_request_approved(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/consult-request-created")
async def consult_request_created(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/consult-completed")
async def consult_completed(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/doctor-connected")
async def doctor_connected(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)

@app.post("/api/events/consult-created")
async def consult_created(
    event: EventCaptureRequest = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return await send_event(event, credentials)
