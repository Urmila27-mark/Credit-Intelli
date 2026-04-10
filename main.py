from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import uvicorn
import json
import os
import tempfile
from datetime import datetime

# Import our modules with error handling
try:
    from pdf_parser import extract_gst_data, extract_bank_data
    from risk_scorer import calculate_risk_score, detect_circular_trading
    from cam_generator import generate_cam
except ImportError as e:
    print(f"⚠️ Warning: Could not import required modules: {e}")
    # Provide fallback functions for testing
    def extract_gst_data(path): return {"company_name": "Unknown", "turnover": 0}
    def extract_bank_data(path): return {"avg_balance": 0, "total_inflows": 0}
    def calculate_risk_score(g, b, c): return {"score": 50, "flags": [], "recommendation": "Review Required"}
    def detect_circular_trading(g, b): return []
    def generate_cam(g, b, r, c): return "CAM summary not available"

app = FastAPI(title="Intelli-Credit API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store analysis results (in-memory for MVP)
analysis_results: Dict[str, Any] = {}

class AnalysisResponse(BaseModel):
    analysis_id: str
    company_name: str
    financial_summary: Dict[str, Any]
    risk_flags: List[Dict[str, Any]]
    risk_score: float
    recommendation: str
    cam_summary: str

def safe_get(data: Optional[Dict], key: str, default: Any = 0) -> Any:
    """Safely get value from dictionary, handling None values"""
    if data is None:
        return default
    value = data.get(key, default)
    return value if value is not None else default

@app.post("/analyze")
async def analyze_company(
    gst_file: UploadFile = File(...),
    bank_file: UploadFile = File(...)
):
    gst_path = None
    bank_path = None
    
    try:
        # Validate file types
        if not gst_file.filename.endswith('.pdf') or not bank_file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Both files must be PDF documents")
        
        # Create temp directory if it doesn't exist
        temp_dir = tempfile.gettempdir()
        
        # Save uploaded files temporarily with safe paths
        gst_path = os.path.join(temp_dir, f"temp_gst_{datetime.now().timestamp()}_{gst_file.filename}")
        bank_path = os.path.join(temp_dir, f"temp_bank_{datetime.now().timestamp()}_{bank_file.filename}")
        
        # Read and save files
        gst_content = await gst_file.read()
        bank_content = await bank_file.read()
        
        if not gst_content or not bank_content:
            raise HTTPException(status_code=400, detail="Uploaded files are empty")
        
        with open(gst_path, "wb") as f:
            f.write(gst_content)
        with open(bank_path, "wb") as f:
            f.write(bank_content)
        
        # Extract data from PDFs
        print("📄 Extracting GST data...")
        gst_data = extract_gst_data(gst_path)
        if not gst_data:
            gst_data = {}
        
        print("📄 Extracting Bank data...")
        bank_data = extract_bank_data(bank_path)
        if not bank_data:
            bank_data = {}
        
        # Detect circular trading
        print("🔄 Detecting circular trading patterns...")
        circular_trading_flags = detect_circular_trading(gst_data, bank_data) or []
        
        # Calculate risk score
        print("📊 Calculating risk score...")
        risk_result = calculate_risk_score(gst_data, bank_data, circular_trading_flags) or {}
        
        # Generate analysis ID
        analysis_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # Added microseconds for uniqueness
        
        # Store results
        analysis_results[analysis_id] = {
            "gst_data": gst_data,
            "bank_data": bank_data,
            "risk_result": risk_result,
            "circular_trading_flags": circular_trading_flags,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate CAM summary
        cam_summary = generate_cam(
            gst_data, 
            bank_data, 
            risk_result, 
            circular_trading_flags
        ) or "CAM summary generation failed"
        
        # Safely get company name with fallback
        company_name = gst_data.get("company_name")
        if not company_name:
            company_name = bank_data.get("company_name", "Unknown")
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            company_name=company_name,
            financial_summary={
                "turnover": safe_get(gst_data, "turnover", 0),
                "gst_mismatch": safe_get(gst_data, "gst_mismatch_percent", 0),
                "bank_balance": safe_get(bank_data, "avg_balance", 0),
                "cash_inflows": safe_get(bank_data, "total_inflows", 0)
            },
            risk_flags=risk_result.get("flags", []) + circular_trading_flags,
            risk_score=risk_result.get("score", 50),
            recommendation=risk_result.get("recommendation", "Review Required"),
            cam_summary=cam_summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temp files
        for path in [gst_path, bank_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"⚠️ Could not remove temp file {path}: {e}")

@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis_results[analysis_id]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "analyses_stored": len(analysis_results)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)