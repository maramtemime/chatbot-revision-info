from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json["message"]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en informatique. Réponds toujours en français de manière claire, simple et pédagogique. Utilise une mise en forme propre en Markdown avec des titres, des listes et des exemples de code bien structurés."},
                {"role": "user", "content": user_msg}
                {"role": "system", "content": "Réponds en français avec une mise en forme claire: titres, listes et exemples de code bien structurés en Markdown."}, 
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)