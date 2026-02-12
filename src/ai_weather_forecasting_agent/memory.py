# memory.py
# This script configures the in-memory checkpointing mechanism for the AI agent.
# Author: Lakshitha Karunaratna

from langgraph.checkpoint.memory import InMemorySaver

# Initialize an InMemorySaver for checkpointing the agent's state.
# This allows the agent to maintain conversational memory across turns
# within a single session. The memory is stored in RAM and is not persistent
# across application restarts.
checkpointer = InMemorySaver()