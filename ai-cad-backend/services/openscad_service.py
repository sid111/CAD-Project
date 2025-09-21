# services/openscad_service.py
import subprocess
import tempfile
import io
import zipfile
import os
import trimesh
import plotly.graph_objects as go

def sanitize_scad(scad_code: str) -> str:
    banned = ["import(", "include", "system", "shell", "file"]
    for b in banned:
        if b.lower() in scad_code.lower():
            raise ValueError(f"Unsafe OpenSCAD code: contains {b}")
    return scad_code

def render_scad_to_stl(scad_code: str):
    scad_code = sanitize_scad(scad_code)
    with tempfile.TemporaryDirectory() as tmpdir:
        scad_path = os.path.join(tmpdir, "model.scad")
        stl_path = os.path.join(tmpdir, "model.stl")

        with open(scad_path, "w") as f:
            f.write(scad_code)

        subprocess.run(
            ["openscad", "-o", stl_path, scad_path],
            check=True,
            capture_output=True
        )

        with open(stl_path, "rb") as f:
            stl_bytes = f.read()
    return stl_bytes

def render_png_from_stl(stl_bytes: bytes):
    # Load STL into trimesh
    mesh = trimesh.load(io.BytesIO(stl_bytes), file_type="stl")
    vertices = mesh.vertices
    faces = mesh.faces
    x, y, z = vertices[:,0], vertices[:,1], vertices[:,2]
    i, j, k = faces[:,0], faces[:,1], faces[:,2]

    fig = go.Figure(
        data=[go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.7)]
    )
    fig.update_layout(scene=dict(xaxis_visible=True, yaxis_visible=True, zaxis_visible=True),
                      width=700, height=600)
    return fig.to_image(format="png", engine="kaleido")

def export_zip(stl_bytes: bytes):
    buf = io.BytesIO()
    png_bytes = render_png_from_stl(stl_bytes)
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("model.stl", stl_bytes)
        zf.writestr("preview.png", png_bytes)
    buf.seek(0)
    return buf
