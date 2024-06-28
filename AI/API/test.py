from flask import Flask, jsonify, request
import requests
import json
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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", "X-use-cache": "false"}

def query(payload):
    """
    This function calls the Llama API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_unique_prompt(previous_questions):
    """
    This function generates a new prompt with different questions.
    """
    questions_str = ", ".join(f'"{q}"' for q in previous_questions)
    return f"Génère moi 2 questions courtes et fermées (oui ou non) en français qui traitent de sujets éco-responsables. Les questions doivent être différentes des suivantes : {questions_str}. Les questions ne doivent pas être orientées sur des sujets trop techniques et doivent être adaptées à des néophytes de l'écologie. Après chaque question, donne également la réponse (oui ou non). Tout doit être encapsulé dans un format JSON avec une clé question et une clé réponse pour chaque objet. Les réponses doivent être au format (true/false)."

@app.route('/generate', methods=['POST'])
def generate_questions():
    previous_questions = []

    all_questions_responses = []
    try:
        with open('questions_responses.json', 'r', encoding='utf-8') as f:
            all_questions_responses = json.load(f)
            previous_questions = [item['question'] for item in all_questions_responses]
    except FileNotFoundError:
        all_questions_responses = []

    prompt = generate_unique_prompt(previous_questions)

    output = query({
        "inputs": prompt,
        "parameters": {
            "max_length": 500,
            "temperature": 0.9,
            "use_cache": False
        }
    })

    generated_text = output[0]['generated_text']
    json_pattern = re.compile(r'\[\s*{.*?}\s*]', re.DOTALL)
    match = json_pattern.search(generated_text)

    new_questions_responses = []
    if match:
        new_questions_responses = json.loads(match.group())
        if isinstance(all_questions_responses, list):
            all_questions_responses.extend(new_questions_responses)
        else:
            all_questions_responses = new_questions_responses
        
        with open('questions_responses.json', 'w', encoding='utf-8') as f:
            json.dump(all_questions_responses, f, ensure_ascii=False, indent=4)

    return jsonify(new_questions_responses)

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        with open('questions_responses.json', 'r', encoding='utf-8') as f:
            questions_responses = json.load(f)
    except FileNotFoundError:
        questions_responses = []

    return jsonify(questions_responses)

if __name__ == '__main__':
    app.run(debug=True)
