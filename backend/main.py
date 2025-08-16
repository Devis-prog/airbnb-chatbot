from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Legge il contenuto del file una sola volta all'avvio
INFO_FILE_PATH = "info_apartment.txt"

if os.path.exists(INFO_FILE_PATH):
    with open(INFO_FILE_PATH, "r", encoding="utf-8") as f:
        apartment_info = f.read()
else:
    apartment_info = "Informazioni dell'appartamento non disponibili al momento."

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

    user_message = req.message
    style_instruction = style_prompt.get(req.style.lower(), "")

    full_prompt = (
        f"{style_instruction}\n"
        f"Di seguito le informazioni sull'appartamento:\n{apartment_info}\n\n"
        f"Ecco la domanda dell'ospite:\n\"{user_message}\"\n\n"
        f"Rispondi in modo adatto, basandoti solo sulle informazioni disponibili."
    )

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sei un assistente per host di Airbnb. Usa solo le informazioni fornite per rispondere."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message.content
        return {"response": reply}
    except Exception as e:
        return {"error": str(e)}
