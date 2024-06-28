import requests
import json
import re

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
    #return f"Génère moi 2 questions courtes et fermées (oui ou non) en français qui traitent de sujets éco-responsables. Les questions doivent être différentes des suivantes : {questions_str}. Les questions ne doivent pas être orientées sur des sujets trop techniques et doivent être adaptées à des néophytes de l'écologie. Après chaque question, donne également la réponse (oui ou non). Tout doit être encapsulé dans un format JSON avec une clé question et une clé réponse pour chaque objet. Les réponses doivent être au format (true/false). Voici un exemple de format attendu :\n\n```json\n[\n  {{\n    \"question\": \"Les plantations d'arbres peuvent aider à lutter contre la pollution de l'air.\",\n    \"response\": true\n  }},\n  {{\n    \"question\": \"Il est préférable de jeter les déchets recyclables dans la poubelle ordinaire.\",\n    \"response\": false\n  }}\n]\n```\n\nVoici les 2 questions que j'ai générées :\n\n```json\n"
    return f"Génère moi 2 questions courtes et fermées (oui ou non) en français qui traitent de sujets éco-responsables. Les questions doivent être différentes des suivantes : {questions_str}. Les questions ne doivent pas être orientées sur des sujets trop techniques et doivent être adaptées à des néophytes de l'écologie. Après chaque question, donne également la réponse (oui ou non). Tout doit être encapsulé dans un format JSON avec une clé question et une clé réponse pour chaque objet. Les réponses doivent être au format (true/false)."

# Read previous questions from the file
previous_questions = []

all_questions_responses = []
try:
    with open('questions_responses.json', 'r', encoding='utf-8') as f:
        all_questions_responses = json.load(f)
        previous_questions = [item['question'] for item in all_questions_responses]
except FileNotFoundError:
    # If the file does not exist, we start with an empty list
    all_questions_responses = []

# Generate prompt
prompt = generate_unique_prompt(previous_questions)

output = query({
    "inputs": prompt,
    "parameters": {
        "max_length": 500,
        "temperature": 0.9,  # Improve creativity
        "use_cache": False  # unuse cache
    }
})

generated_text = output[0]['generated_text']
# print(generated_text)
# exit()

# Extract JSON part from the generated text
json_pattern = re.compile(r'\[\s*{.*?}\s*]', re.DOTALL)
match = json_pattern.search(generated_text)

if match:
    new_questions_responses = json.loads(match.group())
    
    # Ensure all_questions_responses is a list before extending
    if isinstance(all_questions_responses, list):
        all_questions_responses.extend(new_questions_responses)
    else:
        all_questions_responses = new_questions_responses
    
    # Write updated questions and responses to the JSON file
    with open('questions_responses.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions_responses, f, ensure_ascii=False, indent=4)

print("New questions have been added and saved to questions_responses.json.")
