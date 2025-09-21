# streamlit_frontend.py
import streamlit as st
import requests
import zipfile
import io

BACKEND_URL = "http://127.0.0.1:8000/generate"

st.set_page_config(page_title="AI CAD Designer", layout="centered")
st.markdown("<h1 style='text-align: center;'>AI CAD Designer</h1>", unsafe_allow_html=True)

# Mode selector
mode = st.radio("Choose mode:", ["Prompt Mode (AI/Mock)", "SCAD Mode (manual code)"])

if mode == "Prompt Mode (AI/Mock)":
    prompt = st.text_area("Enter your CAD prompt:", "Create a 20mm cube with a 10mm hole")

    if st.button("Generate from Prompt"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating model..."):
                try:
                    resp = requests.post(BACKEND_URL, json={"prompt": prompt}, stream=True, timeout=60)
                    resp.raise_for_status()
                    zip_bytes = resp.content
                    zip_buf = io.BytesIO(zip_bytes)

                    with zipfile.ZipFile(zip_buf) as zf:
                        with zf.open("preview.png") as f:
                            preview_bytes = f.read()
                        with zf.open("model.stl") as f2:
                            stl_bytes = f2.read()

                    st.subheader("Generated 3D Preview")
                    st.image(preview_bytes, use_column_width=True)

                    st.download_button("Download .zip (STL + PNG)", data=zip_bytes,
                                       file_name="cad_model.zip", mime="application/zip")

                    st.download_button("Download model.stl", data=stl_bytes,
                                       file_name="model.stl", mime="application/sla")
                except Exception as e:
                    st.error(f"Generation failed: {e}")

else:  # SCAD Mode
    scad_code = st.text_area("Enter your OpenSCAD code:", 
    "difference() {\n  cube([20,20,20], center=true);\n  cylinder(h=25, r=5, center=true);\n}")

    if st.button("Generate from SCAD"):
        if not scad_code.strip():
            st.warning("Please enter valid SCAD code.")
        else:
            with st.spinner("Rendering SCAD..."):
                try:
                    resp = requests.post(BACKEND_URL, json={"prompt": "SCAD mode", "scad_code": scad_code}, stream=True, timeout=60)
                    resp.raise_for_status()
                    zip_bytes = resp.content
                    zip_buf = io.BytesIO(zip_bytes)

                    with zipfile.ZipFile(zip_buf) as zf:
                        # In SCAD mode, we may not have PNG preview unless you extend backend
                        if "preview.png" in zf.namelist():
                            with zf.open("preview.png") as f:
                                preview_bytes = f.read()
                            st.subheader("Generated 3D Preview")
                            st.image(preview_bytes, use_column_width=True)

                        with zf.open("model.stl") as f2:
                            stl_bytes = f2.read()

                    st.download_button("Download .zip (STL + PNG)", data=zip_bytes,
                                       file_name="cad_model.zip", mime="application/zip")

                    st.download_button("Download model.stl", data=stl_bytes,
                                       file_name="model.stl", mime="application/sla")
                except Exception as e:
                    st.error(f"SCAD rendering failed: {e}")
