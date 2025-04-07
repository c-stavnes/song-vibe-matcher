
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (PyScript needs this)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/vibe-match", methods=["POST"])
def vibe_match():
    data = request.json
    song = data.get("song", "").strip()

    if not song:
        return jsonify({"results": "Please provide a song title."}), 400

    prompt = f"Suggest 5 songs with a similar vibe to '{song}'. List only the song titles and artists."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        reply = response.choices[0].message.content
        return jsonify({"results": reply})
    except Exception as e:
        return jsonify({"results": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
