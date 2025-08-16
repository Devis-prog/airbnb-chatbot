from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class MessageRequest(BaseModel):
    message: str
    style: str

@app.post("/respond")
async def respond(req: MessageRequest):
    style_prompt = {
        "professionale": "Rispondi in modo professionale, chiaro e cortese.",
        "amichevole": "Rispondi in modo amichevole e informale, con un tono rilassato.",
        "gentile": "Rispondi con gentilezza e disponibilità, ma restando neutro."
    }

    prompt = f"{style_prompt.get(req.style.lower(), '')} Ecco il messaggio ricevuto da un ospite su Airbnb:\n\n\"{req.message}\"\n\nRispondi nel modo indicato."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto per host di Airbnb."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = response["choices"][0]["message"]["content"]
        return {"response": reply}
    except Exception as e:
        return {"error": str(e)}
