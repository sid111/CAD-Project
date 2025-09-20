# 🚀 AI-Powered CAD Generator

Turn natural language prompts into 3D models with Generative AI + CAD automation.  
This project integrates **OpenAI**, **OpenSCAD**, and **Streamlit** to enable designers and engineers to quickly generate CAD-ready models without manually coding geometry.

---

## 📌 Problem
Traditional CAD design requires:
- High technical expertise
- Time-consuming manual modeling
- Iterative trial-and-error for basic shapes

This slows down early-stage prototyping and makes 3D design inaccessible to non-experts.

---

## 💡 Solution
We built a **prompt-to-CAD pipeline** where a user simply types:  
> “Create a 20mm cube with a cylindrical hole in the center.”  

The system then:  
1. Uses **Generative AI** to generate OpenSCAD code.  
2. Automatically renders the `.scad` into `.stl` and `.png`.  
3. Displays the 3D preview in a **Streamlit web app**.  
4. Allows the user to **download the model** for further use.  

---

## 🛠️ Tech Stack
- **Backend**: Python, OpenAI API, OpenSCAD CLI  
- **Frontend**: Streamlit (UI), Three.js/Viewer (for 3D preview)  
- **File Outputs**: `.scad`, `.stl`, `.png`  
- **Version Control**: GitHub  

---

## ⚡ Features
- 📝 **Natural Language Input** → Generate 3D models via prompts  
- ⚙️ **AI-to-CAD Conversion** → OpenAI creates OpenSCAD code  
- 🖼️ **Rendering Engine** → Automatic STL + PNG exports  
- 🌐 **Web UI** → Simple interface for prompts & downloads  
- 🔄 **Error Handling** → Fallback cube/sphere models for invalid prompts  

---

## 🚀 Setup & Installation

1. Clone repo:
   ```bash
   git clone https://github.com/your-username/ai-cad-generator.git
   cd ai-cad-generator
