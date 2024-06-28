from flask import Flask, jsonify, request
import requests
import json
import re

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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", "X-use-cache": "false"}

def query(payload):
    """
    This function calls the Llama API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_unique_prompt(previous_questions, difficulty):
    """
    This function generates a new prompt with different questions based on difficulty level.
    """
    questions_str = ", ".join(f'"{q}"' for q in previous_questions)
    difficulty_level = {
        1: "assez faciles, en d'autres termes accessible pour un adulte peu renseigné sur le sujet.",
        2: "difficiles, en d'autres termes, accessibles pour un adulte très bien renseigné sur le sujet",
        3: "très difficiles, en d'autres termes, accessibles pour un expert en la matière "
    }
    difficulty_text = difficulty_level.get(difficulty, "faciles")

   # return f"Génère moi 2 questions courtes et fermées (oui ou non) en français qui traitent de sujets éco-responsables et qui sont {difficulty_text}. Les questions doivent être différentes des suivantes : {questions_str}. Les questions ne doivent pas être orientées sur des sujets trop techniques et doivent être adaptées à des néophytes de l'écologie. Après chaque question, donne également la réponse (oui ou non). Tout doit être encapsulé dans un format JSON avec une clé question et une clé réponse pour chaque objet. Les réponses doivent être au format (true/false)."
    return f"Génère moi 2 questions courtes et fermées (oui ou non) en français qui traitent de sujets éco-responsables et qui sont {difficulty_text}. Fait en sorte que les réponses ne soit pas trop évidentes. Les questions doivent être différentes des suivantes : {questions_str}. Après chaque question, donne également la réponse (oui ou non). Tout doit être encapsulé dans un format JSON avec une clé question et une clé réponse pour chaque objet. Les réponses doivent être au format (true/false)."

@app.route('/generate', methods=['POST'])
def generate_questions():
    difficulty = request.args.get('difficulty', default=1, type=int)

    if difficulty not in [1, 2, 3]:
        return jsonify({"error": "Invalid difficulty level. Please choose 1 (facile), 2 (moyen), or 3 (difficile)."}), 400
    
    # Vider le fichier JSON
    with open('questions_responses.json', 'w', encoding='utf-8') as f:
        json.dump([], f)

    previous_questions = []

    all_questions_responses = []
    try:
        with open('questions_responses.json', 'r', encoding='utf-8') as f:
            all_questions_responses = json.load(f)
            previous_questions = [item['question'] for item in all_questions_responses]
    except FileNotFoundError:
        all_questions_responses = []

    new_questions_responses = []
    for _ in range(8):
        prompt = generate_unique_prompt(previous_questions, difficulty)

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

        if match:
            new_batch = json.loads(match.group())
            new_questions_responses.extend(new_batch)
            previous_questions.extend([item['question'] for item in new_batch])

    if isinstance(all_questions_responses, list):
        all_questions_responses.extend(new_questions_responses)
    else:
        all_questions_responses = new_questions_responses

    return jsonify(new_questions_responses)

@app.route('/questions', methods=['GET'])
def get_questions():
    #clear json
    with open('questions_responses.json', 'w', encoding='utf-8') as f:
        json.dump([], f)
    # Generate new questions by calling the /generate endpoint
    difficulty = request.args.get('difficulty', default=1, type=int)
    
    if difficulty not in [1, 2, 3]:
        return jsonify({"error": "Invalid difficulty level. Please choose 1 (facile), 2 (moyen), or 3 (difficile)."}), 400

    new_questions_responses = generate_questions_internal(difficulty)

    try:
        with open('questions_responses.json', 'r', encoding='utf-8') as f:
            questions_responses = json.load(f)
    except FileNotFoundError:
        questions_responses = []

    # Return all questions including the new ones generated
    return jsonify(questions_responses)

def generate_questions_internal(difficulty):
    previous_questions = []

    all_questions_responses = []
    try:
        with open('questions_responses.json', 'r', encoding='utf-8') as f:
            all_questions_responses = json.load(f)
            previous_questions = [item['question'] for item in all_questions_responses]
    except FileNotFoundError:
        all_questions_responses = []

    new_questions_responses = []
    for _ in range(5):
        prompt = generate_unique_prompt(previous_questions, difficulty)

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

        if match:
            new_batch = json.loads(match.group())
            new_questions_responses.extend(new_batch)
            previous_questions.extend([item['question'] for item in new_batch])

    if isinstance(all_questions_responses, list):
        all_questions_responses.extend(new_questions_responses)
    else:
        all_questions_responses = new_questions_responses

    with open('questions_responses.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions_responses, f, ensure_ascii=False, indent=4)

    return new_questions_responses

if __name__ == '__main__':
    app.run(debug=True)
