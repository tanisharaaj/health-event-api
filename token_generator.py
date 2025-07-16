from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")  # secure!

@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
        <body>
            <h2>Generate JWT Token</h2>
            <form action="/generate" method="post">
                Partner ID: <input type="text" name="partner_id"><br>
                User ID: <input type="text" name="user_id"><br><br>
                <input type="submit" value="Generate Token">
            </form>
        </body>
    </html>
    """

@app.post("/generate", response_class=HTMLResponse)
def generate_token(partner_id: str = Form(...), user_id: str = Form(...)):
    payload = {
        "partner_id": partner_id,
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return f"<h3>Your JWT Token (valid for 1 hour):</h3><p>{token}</p>"

