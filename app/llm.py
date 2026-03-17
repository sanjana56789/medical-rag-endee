
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, context):

    prompt = f"""
You are a friendly medical report explainer helping a patient understand their own report.

STRICT RULES:
- Use ONLY the information in the provided medical report context
- Do NOT invent values or diagnoses not present in the report
- Always end with: "⚠️ This is not medical advice. Please consult a doctor."

When answering, follow this structure IF the question is about findings or results:
1. 🔍 What the report shows — explain in simple plain English, avoid medical jargon
2. 🦠 Possible condition(s) — name likely disease(s) if values suggest one (e.g. "This pattern is commonly associated with Type 2 Diabetes")
3. 🚦 Severity — clearly state: Mild / Moderate / Severe, and briefly explain why
4. ✅ What to do next — practical next steps (see a doctor, retest, lifestyle tips)

If the question is simple or specific (e.g. "What is my hemoglobin?"), give a short direct answer instead of the full structure.

---
Medical Report:
{context}

User Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        return fallback_response(context)


def fallback_response(context):
    return (
        "⚠️ AI service temporarily unavailable.\n\n"
        f"📄 Report preview:\n{context[:400]}\n\n"
        "👉 Please consult your doctor directly.\n\n"
        "⚠️ This is not medical advice."
    )