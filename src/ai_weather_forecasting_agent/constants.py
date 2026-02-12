# constants.py
# This script defines various constants and shared data structures used across the AI agent project.
# Author: Lakshitha Karunaratna

from dataclasses import dataclass

# SYSTEM_PROMPT: This prompt guides the AI agent's persona and capabilities.
# It instructs the agent to act as a pun-speaking weather forecaster
# and informs it about the available tools (`get_weather_for_location`, `get_user_location`).
# It also sets expectations for how the agent should handle location requests.
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.
You can only answer questions related to weather"""

@dataclass
class Context:
    """
    Represents the context for the AI agent, including user-specific information.
    This dataclass is used to pass contextual data to the agent's tools.
    """
    user_id: str