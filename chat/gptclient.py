import openai
import json

with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

ANNOUNCEMENT_PROMPT = config['announcement_prompt']

def build_announcement_prompt(champ_name, kda, ai_score, result):
    stats_section = (
        f"Champion: {champ_name}\n"
        f"KDA: {kda}\n"
        f"AI-Score: {ai_score}\n"
        f"Result: {result}\n"
    )
    return ANNOUNCEMENT_PROMPT + stats_section

class GPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=self.api_key)

    def get_ai_announcement(self, champ_name, kda, ai_score, result):
        ANNOUNCEMENT_PROMPT_FINAL = build_announcement_prompt(champ_name, kda, ai_score, result)
        prompt = ANNOUNCEMENT_PROMPT_FINAL.format(champ_name=champ_name, kda=kda, ai_score=ai_score, result=result)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=1.0
        )
        return response.choices[0].message.content.strip()
