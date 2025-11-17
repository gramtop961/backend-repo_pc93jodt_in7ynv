from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents, DATABASE_URL, DATABASE_NAME
from schemas import Lead, Subscription

app = FastAPI(title="Luxury Brand API", version="1.0.0")

# CORS setup - allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


@app.get("/", response_model=Message)
async def root():
    return Message(message="Luxury Brand API ready")


@app.get("/test")
async def test_connection():
    # Try to fetch collection names to verify DB connectivity
    try:
        leads = await get_documents("lead", limit=1)
        subs = await get_documents("subscription", limit=1)
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
            "connection_status": "connected",
            "collections": [
                "lead" if leads is not None else None,
                "subscription" if subs is not None else None,
            ],
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
            "connection_status": f"error: {str(e)}",
        }


@app.post("/leads", response_model=dict)
async def create_lead(lead: Lead):
    try:
        created = await create_document("lead", lead.model_dump())
        return {"status": "success", "data": created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads", response_model=List[dict])
async def list_leads():
    try:
        return await get_documents("lead", limit=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/subscribe", response_model=dict)
async def subscribe(sub: Subscription):
    try:
        created = await create_document("subscription", sub.model_dump())
        return {"status": "subscribed", "data": created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
