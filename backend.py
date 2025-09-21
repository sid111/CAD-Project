import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_openscad_code(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # compact + cheaper + fast
        messages=[
            {"role": "system", "content": "You are an expert OpenSCAD generator. Output ONLY valid OpenSCAD code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    test_prompt = "Create a cube of size 20mm."
    scad_code = generate_openscad_code(test_prompt)
    print("Generated OpenSCAD Code:\n", scad_code)
