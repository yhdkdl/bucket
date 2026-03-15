import os
import requests
from dotenv import load_dotenv

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

AI_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_bucket_activities(name, location, budget, group_type):

    prompt = f"""
You are an adventure planning AI.

Generate bucket list activities appropriate for this user:

Location: {location}
Budget: {budget}
Group: {group_type}

Return ONLY valid JSON like:
[
  {{ "title": "activity" }},
  {{ "title": "activity" }}
]
"""

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Bucket App"
    }

    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You generate fun real-world adventures."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9
    }

    response = requests.post(AI_URL, headers=headers, json=body)

    data = response.json()

    text = data["choices"][0]["message"]["content"]

    return text