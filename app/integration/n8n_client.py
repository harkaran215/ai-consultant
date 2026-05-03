import requests

def send_to_n8n(data):
    requests.post(
        "http://localhost:5678/webhook/contract",
        json=data
    )