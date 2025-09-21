import trimesh
import zipfile
import io
import plotly.graph_objects as go

def generate_mesh(prompt: str):
    """
    Generate a mesh from a text prompt.
    Right now it always makes a cube as a placeholder.
    """
    mesh = trimesh.creation.box(extents=(20, 20, 20))
    return mesh

def render_mesh(mesh):
    vertices = mesh.vertices
    faces = mesh.faces

    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    i, j, k = faces[:, 0], faces[:, 1], faces[:, 2]

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                i=i, j=j, k=k,
                color="lightblue",
                opacity=0.5,
            )
        ]
    )
    return fig

def export_zip(mesh, fig):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        # STL file
        stl_bytes = mesh.export(file_type="stl")
        zf.writestr("model.stl", stl_bytes)

        # PNG preview
        png_bytes = fig.to_image(format="png")
        zf.writestr("preview.png", png_bytes)

    buffer.seek(0)
    return buffer
