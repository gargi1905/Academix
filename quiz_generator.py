import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_quiz(text):

    prompt = f"""
You are an expert teacher.

Read the following study material and generate EXACTLY 10 multiple-choice questions.

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation outside JSON.

Format:

[
    {{
        "question":"Question here",
        "options":[
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer":"Correct Option",
        "explanation":"Why this answer is correct."
    }}
]

Study Material:

{text[:5000]}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    result = response.choices[0].message.content.strip()

    # Remove markdown if present
    result = result.replace("```json", "")
    result = result.replace("```", "")

    # Extract JSON array
    match = re.search(r"\[.*\]", result, re.DOTALL)

    if not match:
        raise Exception("AI did not return valid JSON.\n\nReturned:\n" + result)

    return json.loads(match.group())