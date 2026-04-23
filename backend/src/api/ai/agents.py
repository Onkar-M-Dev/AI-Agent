from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from api.ai.llms import get_openai_llm
from api.ai.tools import send_me_email, get_unread_emails, research_email


EMAIL_TOOLS_LIST = [
    send_me_email,
    get_unread_emails,
]


def get_email_agent():
    model = get_openai_llm()

    agent = create_react_agent(
        model=model,
        tools=EMAIL_TOOLS_LIST,
        prompt="""
You manage email tasks.

STRICT RULES:

1. ALWAYS extract the recipient email address from the user message.
2. You MUST pass the recipient as 'to_email' when calling send_me_email.
3. NEVER default to your own email unless explicitly mentioned.
4. If no valid email is found, ask the user for it.

5. If the user asks to send an email:
   → You MUST call the send_me_email tool.

6. Invoke the tool exactly once per request.

7. After calling the tool:
   → STOP and return the tool result.

DO NOT:
- Fake sending email
- Say "email sent" without calling the tool
- Ignore the recipient email
""",
        name="email_agent",
    )

    return agent


def get_research_agent():
    model = get_openai_llm()

    agent = create_react_agent(
        model=model,
        tools=[research_email],
        prompt="You are a helpful research assistant for preparing email data",
        name="research_agent",
    )

    return agent


def get_supervisor():
    llm = get_openai_llm()

    email_agent = get_email_agent()
    research_agent = get_research_agent()

    supe = create_supervisor(
        agents=[email_agent, research_agent],
        model=llm,
        prompt="""
You are a supervisor routing requests to specialized agents.

Routing rules:

1. If the user asks to SEND an email,
route to email_agent.

2. If the user asks to DRAFT, WRITE, or COMPOSE an email,
route to email_agent.

3. If the user asks to CHECK INBOX, READ EMAILS, or SUMMARIZE UNREAD EMAILS,
route to email_agent.

4. If the user asks to RESEARCH, GATHER INFORMATION, or SUMMARIZE A TOPIC,
route to research_agent.

5. Always route SEND EMAIL requests to email_agent.

6. Never handle tasks yourself.
Always delegate to one of the agents.
""",
    ).compile()

    return supe