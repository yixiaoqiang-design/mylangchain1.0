from langchain.agents import create_agent
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv()

@tool
def get_available_time_slots(
    attendees: list[str],
    date: str,  # ISO format: "2024-01-15"
    duration_minutes: int
) -> list[str]:
    """Check calendar availability for given attendees on a specific date."""
    # Stub: In practice, this would query calendar APIs
    print ("calendar_agent's tool : get_available_time_slots is called")
    return ["09:00", "14:00", "16:00"]

@tool
def create_calendar_event(
    title: str,
    start_time: str,       # ISO format: "2024-01-15T14:00:00"
    end_time: str,         # ISO format: "2024-01-15T15:00:00"
    attendees: list[str],  # email addresses
    location: str = ""
) -> str:
    """Create a calendar event. Requires exact ISO datetime format."""
    # Stub: In practice, this would call Google Calendar API, Outlook API, etc.
    print ("calendar_agent's tool : create_calendar_event is called")
    return f"Event created: {title} from {start_time} to {end_time} with {len(attendees)} attendees"

CALENDAR_SYSTEM_PROMPT=(
    "You are a calendar scheduling assistant. "
    "Parse natural language scheduling requests (e.g., 'next Tuesday at 2pm') "
    "into proper ISO datetime formats. "
    "Use get_available_time_slots to check availability when needed. "
    "Use create_calendar_event to schedule events. "
    "Always confirm what was scheduled in your final response."
)

calendar_agent = create_agent(
    model="deepseek:deepseek-chat",
    system_prompt=CALENDAR_SYSTEM_PROMPT,
    tools=[get_available_time_slots, create_calendar_event]
)

def test_calendar_agent():
    
    query = "hello"
    for event in calendar_agent.stream(
        {"messages":{"role": "user", "content": query}},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

    query = "Schedule a team meeting ['design-team@abc.com'] on 2025-11-15 at 2pm 1 hour"
    for event in calendar_agent.stream(
        {"messages":{"role": "user", "content": query}},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

# test_calendar_agent()