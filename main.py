from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
from services.glare_service import GlareEvaluatorService

# Create FastAPI app instance
app = FastAPI(title="Smart Blind Solar Glare API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def homepage():
    with open("static/index.html", "r") as f:
        return f.read()

glare_evaluator = GlareEvaluatorService()

@app.get("/api/v1/glare-status")
def get_glare_status(lat, lon, orientation, tz, fov):
    current_time = pd.Timestamp.now(tz=tz)
    is_glaring = await glare_evaluator.evaluate_glare(lat=lat, lon=lon, orientation=orientation, tz=tz, current_time=current_time, fov=fov)
    return is_glaring