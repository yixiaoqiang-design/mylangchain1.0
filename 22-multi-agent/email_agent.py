from langchain.agents import create_agent
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv()

EMAIL_AGENT_PROMPT = (
    "You are an email assistant. "
    "Compose professional emails based on natural language requests. "
    "Extract recipient information and craft appropriate subject lines and body text. "
    "Use send_email to send the message. "
    "Always confirm what was sent in your final response."
)

@tool
def send_email(
    to: list[str],  # email addresses
    subject: str,
    body: str,
    cc: list[str] = []
) -> str:
    """Send an email via email API. Requires properly formatted addresses."""
    # Stub: In practice, this would call SendGrid, Gmail API, etc.
    print ("email_agent's tool : send_email is called")
    return f"Email sent to {', '.join(to)} - Subject: {subject}"

email_agent = create_agent(
    model="deepseek:deepseek-chat",
    system_prompt=EMAIL_AGENT_PROMPT,
    tools=[send_email] 
)

def test_email_agent():
    query = "hello"
    for event in email_agent.stream(
        {"messages":{"role": "user", "content": query}},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

    query = "Send a email to team ['design-team@abc.com'] about reviewing the design document"
    for event in email_agent.stream(
        {"messages":{"role": "user", "content": query}},
        stream_mode="values"
    ):
        event["messages"][-1].pretty_print()

# test_email_agent()