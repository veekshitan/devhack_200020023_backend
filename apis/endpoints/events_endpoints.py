from fastapi import APIRouter, Depends, Request
from models.events_model import EventsModel
from utils.events_utils import save_event, get_events,get_events_by_name
router=APIRouter()

@router.post("/events")
async def add_event(request: EventsModel):
    return save_event(request.roll_number, request.name, request.description,request.image,request.website_link,request.sub_events)
@router.get("/events/{event_name}")
async def get_events_by_main_event(event_name:str):
    return  get_events_by_name(event_name)
@router.get("/events")
async def events():
    return get_events()