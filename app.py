from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from openai import OpenAI

# OpenAI client
client = OpenAI(
    api_key="YOUR_API_KEY"
)

app = FastAPI()

# Request model
class Question(BaseModel):
    question: str

# Database connection
conn = sqlite3.connect("sjbit.db", check_same_thread=False)
cursor = conn.cursor()

@app.get("/")
def home():
    return {"message": "SJBIT Q&A API Running"}

@app.post("/ask")
def ask_question(data: Question):

    user_question = data.question

    # STEP 1: Check database
    cursor.execute(
        "SELECT answer FROM qa WHERE question=?",
        (user_question,)
    )

    result = cursor.fetchone()

    # If answer exists in DB
    if result:
        return {
            "source": "database",
            "answer": result[0]
        }

    # STEP 2: Ask OpenAI
    prompt = f"""
    You are an AI assistant for SJBIT College.

    Rules:
    - Answer ONLY SJBIT-related questions.
    - If the question is unrelated to SJBIT,
      reply:
      "I can answer only SJBIT-related questions."

    - Keep responses short and accurate.
    - Do not make up fake information.

    User Question:
    {user_question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

        return {
            "source": "openai",
            "answer": answer
        }

    except Exception:
        return {
            "source": "openai",
            "answer": "OpenAI quota exceeded or API unavailable."
        }