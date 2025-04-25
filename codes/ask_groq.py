# ask_groq.py

from groq import Groq
from config import GROQ_API_KEY

def ask_groq(question: str, context: str) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
    Berikut adalah isi dokumen medis:

    {context[:3000]}

    Jawab pertanyaan berikut dengan akurat berdasarkan dokumen di atas:

    {question}
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
