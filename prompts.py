import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def skill_to_business_prompt(skill: str, filters=None) -> str:
    prompt = f"I have this skill: {skill}.\nAct like a startup advisor."

    if filters:
        if filters.get("biz_type") != "Any":
            prompt += f"\nOnly suggest {filters['biz_type']} businesses."
        if filters.get("solo"):
            prompt += "\nMake sure each idea can be done solo."

    prompt += (
        "\nGive 5 business ideas. Each one should include:\n"
        "- Catchy title\n"
        "- Short description (1–2 sentences)\n"
        "- Business Type (Online / Offline / Hybrid)\n"
        "- Effort Level (Low / Medium / High)\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful business idea coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=800
    )

    return response['choices'][0]['message']['content']


def follow_up_prompt(previous_output: str, followup: str) -> str:
    prompt = (
        f"Here are the business ideas the user got:\n{previous_output}\n\n"
        f"User follow-up: {followup}\n"
        "Expand on the selected idea and provide helpful extra info."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful business idea explainer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )

    return response['choices'][0]['message']['content']
