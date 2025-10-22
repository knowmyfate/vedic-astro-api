from fastapi import FastAPI
from .utils import get_afflictions, get_compatibility, get_daily_calendar, get_divisional_chart, get_general_predictions, get_nakshatra, get_planet_combinations, get_planet_periods, get_planet_positions

app = FastAPI()

@app.get("/")
def get_msg():    
    return { "message": "Welcome to the Vedic Astrology API" }

@app.post("/aff")
def get_aff(data):
    return get_afflictions(data)

@app.post("/cal")
def get_cal(data):
   return get_daily_calendar(data)

@app.post("/cha")
def get_cha(data):
    return get_divisional_chart(data)

@app.post("/com")
def get_com(data):
    return get_compatibility(data)

@app.post("/nak")
def get_nak(data):
    return get_nakshatra(data)

@app.post("/pl-com")
def get_pl_com(data):
   return get_planet_combinations(data)

@app.post("/pl-per")
def get_pl_per(data):
    return get_planet_periods(data)

@app.post("/pl-pos")
def get_pl_pos(data):
    return get_planet_positions(data)

@app.post("/pre")
def get_pre(data):
    return get_general_predictions(data)
