# model.py
# This script initializes the large language model (LLM) used by the AI agent.
# Author: Lakshitha Karunaratna

from langchain.chat_models import init_chat_model

# Initialize the chat model.
# "gpt-4.1-nano" is specified as the model to use.
# `temperature` controls the randomness of the output: lower values make it more deterministic.
# `timeout` sets a limit for the model's response time.
# `max_tokens` limits the length of the generated response.
model = init_chat_model(
    "gpt-4.1-nano",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)