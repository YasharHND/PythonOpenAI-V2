import json
import random
import webbrowser

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("Generating news...")
response = client.chat.completions.create(
    model="gpt-4o",
    seed=69,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "system", "content": "You are aware of UEFA European Football Championship 2024."},
        {"role": "system", "content": "You are aware that Spain and England are the finalists."},
        {"role": "user", "content": "List some fun news about the finalists of UEFA European Football Championship 2024."}
    ]
)

content = json.loads(response.choices[0].message.content)
spain = [item for item in content["finalists"] if item["team"] == "Spain"][0]
news = spain["news"]
chosen_news_item = random.choice(news)
print("Chosen news item:")
print(json.dumps(chosen_news_item, indent=2))

print("Generating Image...")
response = client.images.generate(
    model="dall-e-3",
    prompt=f"Image for the news with title: {chosen_news_item['title']} and description: {chosen_news_item['description']}",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
print(image_url)
webbrowser.open(image_url)
