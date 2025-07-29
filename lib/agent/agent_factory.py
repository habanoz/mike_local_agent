from typing import Callable
from lib.llm.kllm import Kllm
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

def build_agent(session_id: str, tools: list, config) -> Callable:
    kllm = Kllm(config['llms'])
    checkpointer = InMemorySaver()

    invoke_config = {"configurable": {"thread_id": session_id}}
    invoke_config = set_trace_config(invoke_config, config, session_id)
    
    agent = create_react_agent(
        model=kllm.get_deterministic_llm(),  
        tools=tools if tools else None,  
        prompt="You are a helpful assistant, answer the user's questions. Use provided tools if necessary.",
        checkpointer=checkpointer
    )
            
    def add_message(question, chat_history):
        messages = agent.invoke({"messages": [{"role": "user", "content": question}]}, config=invoke_config)['messages']
        chat_history.clear()
        chat_history.extend(messages)
        return messages[-1].content

    return add_message


def set_trace_config(invoke_config, config, session_id: str):
    if "trace" not in config:
        return invoke_config
    
    trace_config = config["trace"]
    
    if not trace_config.get("enabled", True):
        return invoke_config
    
    if trace_config.get("provider") is None:
        raise ValueError("Trace backend must be specified in the config.")
    
    provider = trace_config["provider"]
    if provider == "langfuse":
        from langfuse.langchain import CallbackHandler
        langfuse_handler = CallbackHandler()
        
        invoke_config["callbacks"] = [langfuse_handler]
        invoke_config["metadata"] = {"langfuse_session_id": session_id}
    
    return invoke_config