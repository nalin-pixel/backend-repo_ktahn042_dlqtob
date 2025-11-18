import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Sermon, Event, Ministry, Story, Leader, ContactMessage, PrayerRequest

app = FastAPI(title="CCBC Murrieta API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "CCBC Murrieta Backend Running"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# Public read endpoints
@app.get("/sermons", response_model=List[Sermon])
def list_sermons(limit: int = 20):
    try:
        docs = get_documents("sermon", {}, limit)
        # Convert ObjectId and datetime to serializable
        return [Sermon(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events", response_model=List[Event])
def list_events(limit: int = 12):
    try:
        now = datetime.utcnow()
        docs = db["event"].find({"start_date": {"$gte": now}}).sort("start_date", 1).limit(limit)
        return [Event(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ministries", response_model=List[Ministry])
def list_ministries():
    try:
        docs = get_documents("ministry")
        return [Ministry(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stories", response_model=List[Story])
def list_stories(limit: int = 6):
    try:
        docs = db["story"].find({}).sort("date", -1).limit(limit)
        return [Story(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Submission endpoints
@app.post("/contact")
def submit_contact(payload: ContactMessage):
    try:
        doc_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/prayer")
def submit_prayer(payload: PrayerRequest):
    try:
        doc_id = create_document("prayerrequest", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
