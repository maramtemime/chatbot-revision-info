from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json["message"]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
       
       # Baddel el partie hedhi f-el code mte3ek:
messages=[
    {
        "role": "system", 
        "content": """Tu es un expert en informatique. 
        Ta mission est UNIQUEMENT de répondre aux questions liées à l'informatique (programmation, réseaux, bases de données, etc.). 
        Si l'utilisateur te pose une question sur un autre sujet (cuisine, sport, musique, etc.), 
        réponds poliment que tu es spécialisé uniquement en informatique et refuse de répondre. 
        Réponds toujours en français."""
    },
    {"role": "user", "content": user_msg}
]
     )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)