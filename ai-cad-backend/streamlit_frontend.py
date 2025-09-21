# streamlit_app.py
import streamlit as st
import requests
import zipfile
import io
import plotly.graph_objects as go
import trimesh

BACKEND_URL = "http://127.0.0.1:8000/generate"

# -----------------------
# Helper: render STL to Plotly
# -----------------------
def render_stl(stl_bytes):
    mesh = trimesh.load(io.BytesIO(stl_bytes), file_type="stl")
    vertices = mesh.vertices
    faces = mesh.faces

    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    i, j, k = faces[:, 0], faces[:, 1], faces[:, 2]

    fig = go.Figure(
        data=[go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color='lightblue', opacity=0.5)]
    )
    fig.update_layout(
        scene=dict(xaxis=dict(visible=True), yaxis=dict(visible=True), zaxis=dict(visible=True)),
        width=700, height=600
    )
    return fig

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="AI CAD Designer", layout="wide")
st.title("🛠️ AI CAD Designer")

mode = st.radio("Choose Mode:", ["Prompt Mode", "SCAD Mode"])

if mode == "Prompt Mode":
    prompt = st.text_area("Enter your CAD prompt:", "")
    if st.button("Generate from Prompt"):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Calling backend..."):
                response = requests.post(BACKEND_URL, json={"prompt": prompt})
                if response.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                        stl_bytes = zf.read("model.stl")
                        fig = render_stl(stl_bytes)
                        st.plotly_chart(fig)
                        st.download_button("Download ZIP", data=response.content,
                                           file_name="cad_model.zip", mime="application/zip")
                else:
                    st.error("Backend error: " + response.text)

elif mode == "SCAD Mode":
    scad_code = st.text_area("Enter your OpenSCAD code:", "")
    if st.button("Generate from SCAD"):
        if not scad_code.strip():
            st.warning("Please enter SCAD code first.")
        else:
            with st.spinner("Calling backend..."):
                response = requests.post(BACKEND_URL, json={"scad_code": scad_code})
                if response.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                        stl_bytes = zf.read("model.stl")
                        fig = render_stl(stl_bytes)
                        st.plotly_chart(fig)
                        st.download_button("Download ZIP", data=response.content,
                                           file_name="cad_model.zip", mime="application/zip")
                else:
                    st.error("Backend error: " + response.text)
