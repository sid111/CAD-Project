# llm_client.py
import os
import re
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in environment")
openai.api_key = OPENAI_KEY

SYSTEM_PROMPT = """
You are an expert OpenSCAD programmer. 
Output ONLY valid OpenSCAD code and NOTHING else.
Allowed constructs: cube(), sphere(), cylinder(), difference(), union(), translate(), rotate().
Use mm units by default. Do not include comments or text.
"""

def clean_response(text: str) -> str:
    """Remove markdown fences and trim whitespace"""
    text = re.sub(r"^```(?:openscad)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text, flags=re.I)
    return text.strip()

def generate_openscad(prompt: str, model="gpt-4o-mini") -> str:
    """Call OpenAI to generate OpenSCAD code"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.15,
        max_tokens=512
    )
    text = resp["choices"][0]["message"]["content"]
    return clean_response(text)
