from pathlib import Path

from fastapi import APIRouter, HTTPException
import json

from app.schemas.static_files import PolicyResponse

router = APIRouter(prefix="/static_files", tags=["static-files"])


@router.get("/privacy", response_model=PolicyResponse)
def get_privacy():
    try:
        with open("data/privacy.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy policy file not found")


@router.get("/agreement", response_model=PolicyResponse)
def get_agreement():
    try:
        with open("data/agreement.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Agreement file not found")
