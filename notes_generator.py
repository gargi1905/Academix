import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_notes(text):

    # Limit text size
    text = text[:10000]


    prompt = f"""
You are Academix AI.

Create clean study notes from the material below.

Format:

# Summary

# Important Concepts

# Definitions

# Key Points

# Exam Questions

# Revision Tips


Study Material:

{text}
"""


    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=2000,

            timeout=60

        )


        return response.choices[0].message.content



    except Exception as e:

        return f"""
❌ Notes generation failed.

Error:
{str(e)}

Please try again.
"""