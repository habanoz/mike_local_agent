import uuid
from collections.abc import Callable

import json
import streamlit as st
import uuid
from Home import show_sidebar
from lib.agent.agent_factory import build_agent
from lib.service.chat_history_service import ChatHistoryService
from lib.st.session_service import SessionService
from lib.st.cached import db_manager, config, prompts_registry, user_file_vector_store
from lib.utils.chain_output_sink import ChainOutputSink
from lib.utils.chat_history_utils import get_files_to_keep
from lib.tool import load_functions

@st.cache_resource
def chat_history_service():
    return ChatHistoryService(db_manager())

def get_available_tools()-> list:
    return [fn for fn_name, fn in load_functions().items()]

def get_chain_sink() -> ChainOutputSink:
    if "chain_sink" not in st.session_state:
        st.session_state["chain_sink"] = ChainOutputSink()

    return st.session_state["chain_sink"]


def get_session_agent() -> Callable:
    if "session_agent" not in st.session_state:
        with st.spinner("Building..."):
            print("Building chat session...")
            session_id = st.session_state["chat_id"]
            st.session_state["session_agent"] = build_agent(session_id=session_id, tools=get_available_tools(), config=config())

    return st.session_state["session_agent"]


@st.experimental_dialog("File")
def display_file(name, content, file):
    st.title(f"File {name}")
    if file: st.write("**File Name**: " + str(file))
    st.write(content)


@st.experimental_dialog("Please wait...")
def wait_failure():
    st.markdown(
        "Due to limitations of the platform, engaging with UI buttons"
        " while generating an answer cancels current request. ")
    st.markdown("Thanks for your understanding.")
    st.markdown("Please refresh the page to start again!")

    if st.button("Close"):
        st.rerun()


@st.experimental_dialog("Debug Info", width="large")
def show_debug(debug):
    if not debug:
        return
    
    tabs = st.tabs([d['name'].replace("prompt", "prmp")[:11] for d in debug])
    for tab, d in zip(tabs, debug):
        with tab:
            st.subheader(d['name'])
            st.write(d['content'])

@st.experimental_dialog("Tools Info", width="large")
def show_tools(tools):
    if not tools:
        return
    
    st.title(f"Tools")
    st.json(tools)
            
def main():
    if "busy" not in st.session_state:
        st.session_state["busy"] = False

    st.markdown(f"### 💬 Chat with your assistant!")

    if "messages" not in st.session_state:
        ui_introduction_message = prompts_registry().instructions["ui_introduction_message"]
        st.session_state["messages"] = [
            {"role": "ai", "content": ui_introduction_message}]
        st.session_state["busy"] = False

    for mi, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            msg_content = message["content"]
            msg_content = msg_content.replace("[[", "`[").replace("]]", "]`")
            st.markdown(msg_content)

            show_buttons(message, 10, "files", mi)

    if prompt := st.chat_input():

        st.session_state["busy"] = True

        if "chat_id" not in st.session_state or not st.session_state["chat_id"]:
            _chat_id = uuid.uuid4()
            st.session_state["chat_id"] = _chat_id
            chat_history_service().add_chat(_chat_id)

        chat_history_service().add_utterance(st.session_state["chat_id"], "human", prompt)
        st.session_state.messages.append({"role": "human", "content": prompt})

        with st.chat_message("human"):
            st.markdown(prompt)

        with st.chat_message('ai'):
            messages = st.session_state.messages
            question = messages[-1]['content']
            chat_history = messages[1:-1]  # first item is introduction, we can skip it.

            with st.spinner("Generating response..."):
                result, tools = get_session_agent()(question, chat_history)

                st.write(result)
                assert isinstance(result, str)

                files = get_chain_sink().get_and_clear_source_files_sink()
                debug = get_chain_sink().get_and_clear_debug_sink()
                files_to_keep = get_files_to_keep(files, result)

            chat_id = st.session_state["chat_id"]
            chat_history_service().add_utterance(chat_id, "ai", result, files=files_to_keep, debug=debug, tool=json.dumps(tools))

            st.session_state.messages.append({"role": "ai", "content": result, "files": files_to_keep, "debug": debug, "tool":tools})

            st.session_state["busy"] = False
            st.rerun()


def show_buttons(message, max_cols, parent_name, parent_index):
    cols = st.columns(max_cols)
    if "files" in message and message["files"]:
        files = message["files"]
        for i in range(len(cols) - 1):
            with cols[i]:
                if len(files) > i:
                    file = files[i]
                    if st.button(file['name'], key=parent_name + str(parent_index) + str(i),
                                 disabled=st.session_state["busy"]):
                        if st.session_state["busy"]:
                            wait_failure()
                        else:
                            display_file(file['name'], file['content'], file['file'] if 'file' in file else None)
                else:
                    st.empty()

    if "debug" in message and message["debug"]:
        debug = message["debug"]
        with cols[-1]:
            if st.button("🪲", key=parent_name + str(parent_index) + str("d"),
                         disabled=st.session_state["busy"]):
                if st.session_state["busy"]:
                    wait_failure()
                else:
                    show_debug(debug)
    
    if "tool" in message and message["tool"]:
        tool = message["tool"]
        with cols[-1]:
            if st.button("🪲", key=parent_name + str(parent_index) + str("t"),
                        disabled=st.session_state["busy"]):
                if st.session_state["busy"]:
                    wait_failure()
                else:
                    show_tools(json.dumps(tool))


if __name__ == '__main__':
    st.set_page_config(page_title="Chat", page_icon="💬")

    with st.sidebar:
        "Chat with your AI assistant!"

    show_sidebar()

    main()
