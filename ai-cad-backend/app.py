# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io

# Import our service helpers
from services.openscad_service import render_scad_to_stl, export_zip as scad_export_zip
from services.cad_service import generate_mesh, export_zip as cad_export_zip

app = FastAPI(title="AI CAD Designer API")

# -----------------------------
# Request Schema
# -----------------------------
class GenerateRequest(BaseModel):
    prompt: str | None = None
    scad_code: str | None = None

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "AI CAD Designer API is running"}

@app.post("/generate")
def generate(req: GenerateRequest):
    """
    Generates a CAD model from either:
    - Natural language prompt (Prompt Mode)
    - Raw OpenSCAD code (SCAD Mode)
    Returns a .zip containing model.stl + preview.png
    """

    # Mode B: OpenSCAD (if scad_code provided)
    if req.scad_code:
        try:
            stl_bytes = render_scad_to_stl(req.scad_code)
            zip_buf = scad_export_zip(stl_bytes)
            return StreamingResponse(
                zip_buf,
                media_type="application/zip",
                headers={"Content-Disposition": "attachment; filename=cad_model.zip"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenSCAD error: {e}")

    # Mode A: Prompt (default)
    if req.prompt:
        try:
            mesh = generate_mesh(req.prompt)
            zip_buf = cad_export_zip(mesh)
            return StreamingResponse(
                zip_buf,
                media_type="application/zip",
                headers={"Content-Disposition": "attachment; filename=cad_model.zip"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"CAD generation error: {e}")

    # If neither provided
    raise HTTPException(status_code=400, detail="Either prompt or scad_code must be provided")
