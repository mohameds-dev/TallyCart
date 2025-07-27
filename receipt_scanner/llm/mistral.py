import requests

def get_response(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False 
        }
    )
    return response.json()["response"]
