# main.py
# This script serves as the interactive entry point for the AI Weather Forecasting Agent.
# Author: Lakshitha Karunaratna

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from .model import model
from .memory import checkpointer
from .constants import SYSTEM_PROMPT, Context
from .response import ResponseFormat
from .tools import get_user_location, get_weather_for_location

# Initialize the AI agent with its model, system prompt, tools, and context/response schemas.
# The checkpointer is used for managing conversation memory.
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# Configure the conversation thread.
# The `thread_id` is a unique identifier for a given conversation session.
# Using a fixed ID here means the agent will maintain context across messages
# within this single interactive session.
config = {"configurable": {"thread_id": "1"}}

print("Starting interactive weather agent. Type 'exit' or 'quit' to end the conversation.")

# Main interactive loop for conversation with the agent.
while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        print("Ending conversation.")
        break

    # Invoke the agent with the user's message.
    # The `config` maintains the conversation thread, and `context` provides user-specific info.
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config=config,
        context=Context(user_id="1") # Using a dummy user_id="1" for this interactive session.
    )

    # Print the agent's punny response.
    print(f"Agent: {response['structured_response'].punny_response}")