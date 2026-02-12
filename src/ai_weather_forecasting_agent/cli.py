# Author: Lakshitha Karunaratna
import argparse
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from .constants import SYSTEM_PROMPT, Context
from .tools import get_user_location, get_weather_for_location
from .response import ResponseFormat
from .model import model
from .memory import checkpointer


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI Weather Forecasting Agent CLI")
    parser.add_argument("location", nargs="?", default=None, help="Location to forecast")
    args = parser.parse_args(argv)

    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer
    )

    # Use a fixed thread_id for CLI for simplicity
    config = {"configurable": {"thread_id": "cli_session"}}

    messages = []
    if args.location:
        messages.append({"role": "user", "content": f"what is the weather in {args.location}?"})
    else:
        messages.append({"role": "user", "content": "what is the weather outside?"})


    response = agent.invoke(
        {"messages": messages},
        config=config,
        context=Context(user_id="1") # Using a dummy user_id for CLI
    )

    print(f"Punny Response: {response['structured_response'].punny_response}")
    if response['structured_response'].weather_conditions:
        print(f"Weather Conditions: {response['structured_response'].weather_conditions}")


if __name__ == "__main__":
    main()
