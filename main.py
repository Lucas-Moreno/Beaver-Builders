import requests
import json

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "génère un JSON avec comme élément une question et une réponse qui est soit true soit false",
})

generated_text = output[0]['generated_text']
print()
start_index = generated_text.find('```json\n') + len('```json\n')
end_index = generated_text.find('```\n', start_index)

json_str = generated_text[start_index:end_index].strip()

json_data = json.loads(json_str)

with open('data.json', 'w') as f:
    json.dump(json_data, f, indent=4)

print("Le contenu JSON a été écrit dans le fichier data.json avec succès.")
