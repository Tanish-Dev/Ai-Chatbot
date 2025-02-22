import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="gpt-3.5-turbo-instruct",
  prompt="",
  temperature=1,
  max_tokens=256,
  top_p=1,
)
print(response)
