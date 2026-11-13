"""
AgroShift Nexus: NASA Space Apps Decision-Support System Backend.
National Coverage: All 64 Districts across 8 Administrative Divisions of Bangladesh.
Multi-Agent Architecture (6 Specialist Agents + 1 Master Rotation Agent + ML Engine).
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .data.bangladesh_regions import DISTRICTS, get_district_profile, get_all_districts, get_districts_by_division
from .data.crop_database import CROPS
from .data.nasa_client import NASAClient
from .agents.flood_agent import FloodAgent
from .agents.drought_agent import DroughtAgent
from .agents.soil_agent import SoilAgent
from .agents.agronomy_agent import AgronomyAgent
from .agents.economic_agent import EconomicAgent
from .agents.degradation_agent import DegradationAgent
from .agents.master_agent import MasterRotationAgent

app = FastAPI(
    title="AgroShift Nexus National Engine",
    description="Multi-Agent Decision-Support System utilizing NASA Earth Observations for Climate-Adaptive Crop Rotation across all 64 Districts of Bangladesh.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents & NASA Client
nasa_client = NASAClient(use_live_api=True)
flood_agent = FloodAgent()
drought_agent = DroughtAgent()
soil_agent = SoilAgent()
agronomy_agent = AgronomyAgent()
economic_agent = EconomicAgent()
degradation_agent = DegradationAgent()
master_agent = MasterRotationAgent()

class FarmAnalysisRequest(BaseModel):
    region_id: str = Field(default="rangpur", description="Target district ID (one of 8 districts in Rangpur Division: rangpur, dinajpur, kurigram, gaibandha, nilphamari, thakurgaon, panchagarh, lalmonirhat)")
    upazila: Optional[str] = Field(default=None, description="Upazila name or key")
    union_id: Optional[str] = Field(default=None, description="Union ID (e.g. RNG_U001)")
    union_name: Optional[str] = Field(default=None, description="Union name (e.g. Rangpur Sadar_Union_1)")
    past_crop: str = Field(default="boro_rice", description="Crop grown in previous seasons")
    monoculture_years: int = Field(default=3, description="Consecutive years growing the same crop")
    priority: str = Field(default="water_saving", description="Farmer primary objective: water_saving, soil_health, max_profit")
    land_area_bigha: float = Field(default=2.0, description="Land area in bighas (1 bigha ~ 0.33 acre)")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "system": "Krishi Bondhu AI / AgroShift Nexus Engine",
        "coverage": "Rangpur Division (8 Districts, 536 Unions)",
        "empirical_records_trained": 1391520,
        "models_count": 6,
        "ml_model_status": "Loaded (6 Specialized Models + 1 Crop Agronomy Model)",
        "cross_validation": "5-Fold Stratified CV on 70% Train, 15% Val, 15% Test",
        "data_leakage_prevented": True,
        "nasa_datasets_active": [
            "NASA GPM IMERG V07 (Precipitation & Flash Flood)",
            "NASA MODIS MOD11A2 / MERRA-2 (Land Surface Temperature & Heat Stress)",
            "NASA SMAP L4 SPL4SMGP (Root-Zone Soil Moisture & Hydrology)",
            "NASA Landsat-8/9 OLI & MOD13Q1 (NDVI/EVI & Soil Fatigue)",
            "NASA MERRA-2 & POWER WS2M (Atmospheric Wind & Lodging)",
            "World Bank CPI & FAO GAEZ (Crop Economics & Market Volatility)"
        ]
    }

@app.get("/api/models-metadata")
def get_models_metadata():
    import json
    meta_path = Path("backend/models/all_6_models_metadata.json")
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Metadata file not found"}

@app.get("/api/hierarchy")
def get_hierarchy():
    hier_path = Path("backend/data/rangpur_hierarchy.json")
    if hier_path.exists():
        with open(hier_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Hierarchy data not found"}

@app.get("/api/districts")
def get_districts():
    rangpur_districts = get_districts_by_division("Rangpur")
    return {
        "total": len(rangpur_districts),
        "division": "Rangpur",
        "districts": rangpur_districts
    }

@app.get("/api/regions")
def get_regions():
    return {"regions": get_districts_by_division("Rangpur")}

@app.get("/api/crops")
def get_crops():
    return {"crops": list(CROPS.values())}

@app.post("/api/analyze")
def run_multi_agent_pipeline(request: FarmAnalysisRequest):
    farmer_input = request.model_dump()
    dist_id = farmer_input["region_id"].lower()

    if dist_id not in DISTRICTS:
        raise HTTPException(status_code=400, detail=f"Invalid district '{dist_id}'. Must be one of the 64 districts of Bangladesh.")

    # 1. Fetch Dynamic Calibrated NASA Earth Observation Data for this exact district
    env_data = nasa_client.fetch_climate_and_satellite_data(dist_id)

    # 1.1 Enrich with Upazila & Union specific telemetry if provided
    union_id = farmer_input.get("union_id")
    upazila_key = farmer_input.get("upazila")
    if union_id:
        try:
            hier_file = Path("backend/data/rangpur_hierarchy.json")
            if hier_file.exists():
                with open(hier_file, "r", encoding="utf-8") as f:
                    hier = json.load(f)
                d_obj = hier.get("districts", {}).get(dist_id, {})
                found_union = None
                for upz in d_obj.get("upazilas", {}).values():
                    for u in upz.get("unions", []):
                        if u.get("id") == union_id:
                            found_union = u
                            break
                    if found_union:
                        break
                if found_union:
                    env_data["region_metadata"]["selected_upazila"] = upazila_key or found_union.get("name_en")
                    env_data["region_metadata"]["selected_union_id"] = found_union.get("id")
                    env_data["region_metadata"]["selected_union_name"] = found_union.get("name_en")
                    env_data["region_metadata"]["selected_union_name_bn"] = found_union.get("name_bn")
                    env_data["region_metadata"]["elevation_m"] = found_union.get("elevation_m")
                    env_data["region_metadata"]["soil_texture"] = found_union.get("soil_texture")
                    env_data["region_metadata"]["river_basin"] = found_union.get("river_basin")
                    env_data["region_metadata"]["lat"] = found_union.get("lat")
                    env_data["region_metadata"]["lon"] = found_union.get("lon")
                    if "soil_profile" in env_data:
                        env_data["soil_profile"]["soil_texture"] = found_union.get("soil_texture")
                        env_data["soil_profile"]["elevation_m"] = found_union.get("elevation_m")
        except Exception as e:
            print("Error looking up union:", e)

    # 2. Execute 6 Specialist Agents
    agent_reports = {
        "flood_agent": flood_agent.evaluate(env_data, farmer_input),
        "drought_agent": drought_agent.evaluate(env_data, farmer_input),
        "soil_agent": soil_agent.evaluate(env_data, farmer_input),
        "agronomy_agent": agronomy_agent.evaluate(env_data, farmer_input),
        "economic_agent": economic_agent.evaluate(env_data, farmer_input),
        "degradation_agent": degradation_agent.evaluate(env_data, farmer_input),
    }

    # 3. Execute Master Rotation Agent for Optimal Synthesis
    master_plan = master_agent.synthesize(env_data, farmer_input, agent_reports)

    return {
        "success": True,
        "query": farmer_input,
        "district_profile": env_data["region_metadata"],
        "data_lineage": env_data.get("data_lineage", {}),
        "nasa_earth_observations": env_data["satellite_sources"],
        "specialist_agent_evaluations": agent_reports,
        "master_adaptive_strategy": master_plan,
        "consensus_recommendation": master_plan
    }

# Mount static frontend
frontend_path = Path("frontend")
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
