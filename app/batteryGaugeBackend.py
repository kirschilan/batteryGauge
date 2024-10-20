from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a model for incoming login requests
class LoginRequest(BaseModel):
    username: str
    password: str

# Simulate a token-based login for now
@app.post("/login")
async def login(request: LoginRequest):
    # Replace with actual iCloud authentication later
    if request.username == "test" and request.password == "password":
        return {"token": "fake-token-123"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Simulate fetching battery data
@app.get("/battery_status")
async def get_battery_status(token: str):
    if token != "fake-token-123":
        raise HTTPException(status_code=403, detail="Invalid token")
    # Replace with real iCloud data later
    return {
        "devices": [
            {"name": "iPhone 12", "battery": 87},
            {"name": "iPad Pro", "battery": 75},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
