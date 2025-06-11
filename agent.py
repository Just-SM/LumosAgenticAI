from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

from langchain_core.tools import tool

load_dotenv()  # Load environment variables (e.g., API keys)


# Define a simple tool decorated with @tool so it can be used by the agent.
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Initialize language model (LLM) to be used by the agent.
llm = init_chat_model(model="gpt-4o-mini", model_provider='openai')


# Define a class to store the agent's state during the graph execution.
# Here it contains the question and the answer.
class AgentState(dict):
    question: str = ""
    answer: str = ""


# Define a function representing the agent node in the graph.
# It receives the current state, creates a react agent that uses the multiply tool,
# constructs the prompt, invokes the agent, and updates the state with the answer.
def agent(state):
    # Create an agent with the multiply tool available
    agent = create_react_agent(llm, tools=[multiply])

    AGENT_PROMPT = 'You are a multi purpose agent. Complete the task, use the tools if possible.'

    AGENT_QUERY = f"Task is: {state['question']}"

    inputs = {
        "messages": [
            ("system", AGENT_PROMPT),
            ("user", AGENT_QUERY)
        ]
    }

    react_res = agent.invoke(inputs)

    # Debug output to see the response and type
    print(react_res)
    print(type(react_res))

    # Return a new state with the answer updated
    return AgentState({**state, "answer": react_res.get('messages')[-1].content})


# Create the state graph builder with AgentState type
builder = StateGraph(AgentState)

# Add the agent node to the graph - this node will execute the agent function
builder.add_node("agent", agent)

# Set the entry point (start of graph execution)
builder.set_entry_point("agent")

# Add an edge from the agent node to END (terminal node)
builder.add_edge("agent", END)

# Compile the graph (finalize it for execution)
graph = builder.compile()


def run_agent(question: str) -> str:
    """Run the graph with a question and return the agent's answer."""
    result = graph.invoke({"question": question})
    print(result)
    return result.get("answer", "No answer generated.")




