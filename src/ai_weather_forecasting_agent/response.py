# response.py
# This script defines the structured output format for the AI agent's responses.
# Author: Lakshitha Karunaratna

from dataclasses import dataclass

# ResponseFormat: This dataclass defines the schema for the AI agent's structured output.
# Using a dataclass (or Pydantic model) ensures that the agent's responses conform to a predictable structure,
# which is essential for consistent processing and display.
@dataclass
class ResponseFormat:
    """
    Response schema for the AI agent.
    The agent is configured to return its output in this specific format.
    """
    # A punny response related to the weather, always required to maintain the agent's persona.
    punny_response: str
    # Optional field to provide interesting information about the weather conditions, if available.
    weather_conditions: str | None = None