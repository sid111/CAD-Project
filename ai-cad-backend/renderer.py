# renderer.py
import subprocess
from pathlib import Path
import uuid

ROOT = Path(__file__).parent
SCAD_DIR = ROOT / "outputs" / "scad"
STL_DIR = ROOT / "outputs" / "stl"
PNG_DIR = ROOT / "outputs" / "png"

for d in (SCAD_DIR, STL_DIR, PNG_DIR):
    d.mkdir(parents=True, exist_ok=True)

def save_scad(code: str, name: str=None) -> Path:
    """Save SCAD code to file"""
    if name is None:
        name = str(uuid.uuid4())[:8]
    scad_path = SCAD_DIR / f"{name}.scad"
    scad_path.write_text(code, encoding="utf-8")
    return scad_path

def run_openscad(scad_path: Path, name: str=None, timeout=20):
    """Render .scad into .stl and .png"""
    if name is None:
        name = scad_path.stem
    stl_path = STL_DIR / f"{name}.stl"
    png_path = PNG_DIR / f"{name}.png"

    # Render STL
    subprocess.run(
        ["openscad", "-o", str(stl_path), str(scad_path)],
        check=True, timeout=timeout
    )

    # Render PNG preview
    subprocess.run(
        ["openscad", "-o", str(png_path), str(scad_path)],
        check=True, timeout=timeout
    )

    return stl_path, png_path
