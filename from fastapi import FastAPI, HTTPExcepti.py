from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Activity(BaseModel):
    id: int
    name: str
    participants: List[str] = []

class Signup(BaseModel):
    email: str

activities = []

@app.post("/api/activities/")
async def create_activity(activity: Activity):
    activities.append(activity.dict())
    return {"message": "Activity created", "activity": activity}

@app.get("/api/activities/")
async def get_activities():
    return activities

@app.post("/api/activities/{activity_id}/signup")
async def signup_for_activity(activity_id: int, signup: Signup):
    activity = next((a for a in activities if a["id"] == activity_id), None)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if signup.email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already registered")
    activity["participants"].append(signup.email)
    return {"message": "Signup successful"}
