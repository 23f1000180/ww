from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Telemetry data from q-vercel-latency.json
DATA = [
    {"region": "apac", "service": "support", "latency_ms": 156.92, "uptime_pct": 97.421},
    {"region": "apac", "service": "analytics", "latency_ms": 183.43, "uptime_pct": 99.495},
    {"region": "apac", "service": "checkout", "latency_ms": 184.7, "uptime_pct": 99.321},
    {"region": "apac", "service": "support", "latency_ms": 142.98, "uptime_pct": 98.33},
    {"region": "apac", "service": "recommendations", "latency_ms": 176.47, "uptime_pct": 99.044},
    {"region": "apac", "service": "recommendations", "latency_ms": 131.34, "uptime_pct": 97.42},
    {"region": "apac", "service": "support", "latency_ms": 144.07, "uptime_pct": 97.174},
    {"region": "apac", "service": "catalog", "latency_ms": 169.9, "uptime_pct": 98.959},
    {"region": "apac", "service": "recommendations", "latency_ms": 163.46, "uptime_pct": 98.824},
    {"region": "apac", "service": "checkout", "latency_ms": 123.07, "uptime_pct": 97.961},
    {"region": "apac", "service": "payments", "latency_ms": 204.25, "uptime_pct": 98.933},
    {"region": "apac", "service": "recommendations", "latency_ms": 178.01, "uptime_pct": 97.523},
    {"region": "emea", "service": "catalog", "latency_ms": 145.66, "uptime_pct": 97.406},
    {"region": "emea", "service": "recommendations", "latency_ms": 130.92, "uptime_pct": 99.029},
    {"region": "emea", "service": "support", "latency_ms": 116.83, "uptime_pct": 98.588},
    {"region": "emea", "service": "checkout", "latency_ms": 127.5, "uptime_pct": 98.415},
    {"region": "emea", "service": "recommendations", "latency_ms": 173.2, "uptime_pct": 97.96},
    {"region": "emea", "service": "payments", "latency_ms": 199.81, "uptime_pct": 98.502},
    {"region": "emea", "service": "support", "latency_ms": 156.24, "uptime_pct": 99.156},
    {"region": "emea", "service": "catalog", "latency_ms": 118.63, "uptime_pct": 99.464},
    {"region": "emea", "service": "checkout", "latency_ms": 220.64, "uptime_pct": 98.807},
    {"region": "emea", "service": "checkout", "latency_ms": 106.77, "uptime_pct": 98.855},
    {"region": "emea", "service": "support", "latency_ms": 200.24, "uptime_pct": 98.094},
    {"region": "emea", "service": "payments", "latency_ms": 182.82, "uptime_pct": 97.358},
    {"region": "amer", "service": "recommendations", "latency_ms": 230.81, "uptime_pct": 99.304},
    {"region": "amer", "service": "checkout", "latency_ms": 181.02, "uptime_pct": 97.86},
    {"region": "amer", "service": "recommendations", "latency_ms": 135, "uptime_pct": 97.859},
    {"region": "amer", "service": "recommendations", "latency_ms": 178.61, "uptime_pct": 98.719},
    {"region": "amer", "service": "payments", "latency_ms": 192.85, "uptime_pct": 97.731},
    {"region": "amer", "service": "catalog", "latency_ms": 214.97, "uptime_pct": 98.574},
    {"region": "amer", "service": "payments", "latency_ms": 202.58, "uptime_pct": 98.321},
    {"region": "amer", "service": "payments", "latency_ms": 153.08, "uptime_pct": 97.738},
    {"region": "amer", "service": "analytics", "latency_ms": 180.03, "uptime_pct": 98.905},
    {"region": "amer", "service": "checkout", "latency_ms": 122.74, "uptime_pct": 98.886},
    {"region": "amer", "service": "analytics", "latency_ms": 187.38, "uptime_pct": 98.332},
    {"region": "amer", "service": "support", "latency_ms": 205.76, "uptime_pct": 98.123}
]

@app.post("/api/metrics")
async def get_metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)
    
    response = {}
    for r in regions:
        # Filter data for specific region
        subset = [d for d in DATA if d["region"] == r]
        if not subset: continue
        
        lats = [d["latency_ms"] for d in subset]
        uptimes = [d["uptime_pct"] for d in subset]
        
        response[r] = {
            "avg_latency": round(float(np.mean(lats)), 2),
            "p95_latency": round(float(np.percentile(lats, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 3),
            "breaches": sum(1 for l in lats if l > threshold)
        }
    return response