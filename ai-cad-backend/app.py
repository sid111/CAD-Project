from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from services.cad_service import generate_mesh, render_mesh, export_zip

app = FastAPI(title="AI CAD Backend")

@app.get("/")
def root():
    return {"message": "AI CAD Backend is running!"}

@app.post("/generate")
def generate(prompt: str):
    # Step 1: Generate a mesh
    mesh = generate_mesh(prompt)

    # Step 2: Render with plotly
    fig = render_mesh(mesh)

    # Step 3: Package as zip
    zip_buffer = export_zip(mesh, fig)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=cad_model.zip"}
    )
