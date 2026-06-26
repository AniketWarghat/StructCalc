from fastapi import FastAPI
from schemas.input_models import BeamDesignInput
from modules.beam.beam_is456 import design_beam_is456

# Initialize your core FastAPI web Server application
app = FastAPI(
    title="StructCalc Calculation Engine",
    description="Python FastAPI service handling structural design routines.",
    version="1.0"
)

#1. Health Check ENdpoint
@app.get("/health")
def health_check():
    return{"status": "healthy", "service":"StructCalc-engine"}

#2. Structural Beam Calculation
@app.post("/calc/beam")
def calculate_beam(payload: BeamDesignInput):
    results = design_beam_is456(payload)
    return results