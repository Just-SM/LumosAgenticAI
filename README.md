
Instalation

- create a Python Virtual Environment (optional but recommended)

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
> or
venv\Scripts\activate     # Windows

- run `pip install -r requirements.txt`

- run `streamlit run app.py`

- add key to .env

# Tasks 
1. Make following operation work (with tools)
- "Multiply 5 by 7" 
- "What is 12 - 9?" 
- "Please multiply 3 and 4, then add 2 to the result."

2. Add one more step in graph processing. For example: formatting output of Agent to "Agent response: {answer}"

3. *Optional* add some ready tools form LangChain - tools. And test them)



# Hints

1. Adding New Tools:
   - Define a new function that performs some action.
   - Add the @tool decorator from langchain_core.tools.
   - Add this new tool to the list of tools passed to create_react_agent().
   Example:

   @tool
   def add(a: int, b: int) -> int:
       '''Add two numbers.'''
       return a + b
   
   ### Later in agent function:
   agent = create_react_agent(llm, tools=[multiply, add])

2. Adding More Steps to the Graph:
   - Define more functions that accept and transform the AgentState.
   - Add them as nodes using builder.add_node("node_name", function).
   - Connect nodes using builder.add_edge("from_node", "to_node").
   - Set the entry point to the first node you want to run.
   
   Example:
   def pre_process(state):
       # do some preprocessing on state
       return state

   def post_process(state):
       # do some postprocessing
       return state

   builder.add_node("pre", pre_process)
   builder.add_node("agent", agent)
   builder.add_node("post", post_process)

   builder.set_entry_point("pre")
   builder.add_edge("pre", "agent")
   builder.add_edge("agent", "post")
   builder.add_edge("post", END)
