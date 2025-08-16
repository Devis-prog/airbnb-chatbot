from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Imposta la tua chiave OpenAI (verrà inserita come variabile d'ambiente su Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Crea l'app
app = FastAPI()

# CORS per permettere accesso dall'estensione
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Per sicurezza, puoi restringerlo dopo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funzione per leggere il file info_apartment.txt
def get_apartment_info():
    try:
        with open("info_apartment.txt", "r") as file:
            return file.read()
    except:
        return "Nessuna informazione disponibile."

# Endpoint principale
@app.post("/generate")
async def generate_response(req: Request):
    data = await req.json()
    messaggio = data.get("messaggio")
    stile = data.get("stile", "gentile")
    contesto = get_apartment_info()

    prompt = f"""
Hai ricevuto questo messaggio da un ospite Airbnb:
\"{messaggio}\"

Queste sono le informazioni sulla casa:
\"\"\"{contesto}\"\"\"

Scrivi una risposta {stile}, utile, chiara e professionale.
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0.7
        )
        risposta = completion.choices[0].message.content
        return { "risposta": risposta }
    except Exception as e:
        return { "errore": str(e) }
