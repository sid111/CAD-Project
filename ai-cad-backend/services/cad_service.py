# services/cad_service.py
import io
import zipfile
import trimesh
import plotly.graph_objects as go

def create_cube(size=20.0):
    return trimesh.creation.box(extents=(size, size, size))

def render_mesh_png(mesh):
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

def export_zip(mesh, png_bytes):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("model.stl", mesh.export(file_type="stl"))
        zf.writestr("preview.png", png_bytes)
    buf.seek(0)
    return buf
