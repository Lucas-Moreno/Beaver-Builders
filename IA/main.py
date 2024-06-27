import requests
import json
import os
from functions.update_json import update_json

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

json_file = 'data.json'

def extract_question_answer(generated_text):
    start_question = "**Question** : "
    end_question = "\n\n**Réponse** : "
    start_answer = "\n\n**Réponse** : **"
    end_answer = "**"

    start_question_idx = generated_text.find(start_question) + len(start_question)
    end_question_idx = generated_text.find(end_question)
    start_answer_idx = generated_text.find(start_answer) + len(start_answer)
    end_answer_idx = generated_text.find(end_answer, start_answer_idx)

    question = generated_text[start_question_idx:end_question_idx].strip()
    answer = generated_text[start_answer_idx:end_answer_idx].strip()

    question_answer_obj = {
        "question": question,
        "answer": answer.lower() == 'true'
    }
    
    return question_answer_obj

def main(number_of_questions):
    new_questions = []

    for _ in range(number_of_questions):
        output = query({
            "inputs": "écrit une seule question en français basé sur l'écologie et sa réponse qui est soit true soit false",
        })

        generated_text = output[0]['generated_text']
        question_answer_obj = extract_question_answer(generated_text)
        new_questions.append(question_answer_obj)
    
    new_object = {"questions": new_questions}
    update_json(json_file, new_object, None)

if __name__ == "__main__":
    number_of_questions = 10
    main(number_of_questions)
