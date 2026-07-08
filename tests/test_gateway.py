# test_gateway.py

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LITELLM_TOKEN"),
    base_url="https://litellm.oit.duke.edu/v1"
)

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {
            "role": "user",
            "content": "Reply with only the word SUCCESS."
        }
    ]
)

print(response.choices[0].message.content)