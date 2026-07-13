import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_pdf(question, pdf_text):

    prompt = f"""
You are Academix AI.

Answer ONLY using the study material below.

If the answer is not found in the study material, reply:

"I couldn't find this information in the uploaded PDF."

Study Material:

{pdf_text[:12000]}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    print(response)
    print(response.choices[0].message)
    return response.choices[0].message.content