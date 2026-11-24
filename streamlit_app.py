import os

import streamlit as st
from groq import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    Groq,
    RateLimitError,
)
from streamlit.errors import StreamlitSecretNotFoundError


MODELS = {
    "GPT-OSS 120B": "openai/gpt-oss-120b",
    "GPT-OSS 20B": "openai/gpt-oss-20b",
    "Qwen 3.8 27B": "qwen/qwen3.8-27b",
}

SYSTEM_PROMPT = (
    "You are a helpful study assistant. Explain ideas clearly and answer "
    "the user's question directly. Admit uncertainty and do not invent "
    "references. You have no access to uploaded documents or live web "
    "search. Keep answers under 150 words unless the user requests more."
)


def configured_api_key():
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        return key

    try:
        return st.secrets.get("GROQ_API_KEY", "").strip()
    except StreamlitSecretNotFoundError:
        return ""


def request_answer(api_key, model_id, history, question):
    client = Groq(api_key=api_key, timeout=60.0, max_retries=0)

    if model_id.startswith("openai/gpt-oss-"):
        options = {
            "reasoning_effort": "low",
            "include_reasoning": False,
        }
    else:
        options = {
            "reasoning_effort": "default",
            "reasoning_format": "hidden",
        }

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-12:],
            {"role": "user", "content": question},
        ],
        max_completion_tokens=4096,
        **options,
    )

    if not response.choices:
        raise ValueError("No answer was returned. Please try again.")

    answer = (response.choices[0].message.content or "").strip()

    if not answer:
        raise ValueError("The model returned an empty answer. Please try again.")

    return answer


def main():
    st.set_page_config(
        page_title="Research and Study Assistant — Without RAG",
        page_icon="💬",
    )

    st.title("Research and Study Assistant — Without RAG")
    st.write("Choose a model and ask a study question.")
    st.caption(
        "Answers use the model's learned knowledge and recent conversation. "
        "No documents are uploaded or retrieved."
    )

    with st.sidebar:
        st.header("Choose your LLM")
        model_name = st.selectbox("Language model", list(MODELS))

        st.caption("All three models are hosted by Groq.")
        st.caption("Changing the model starts a new conversation.")

        with st.expander("Groq API key (optional)"):
            personal_key = st.text_input(
                "Groq API key",
                type="password",
                key="personal_groq_key",
                help="Leave blank if a key is already configured for this app.",
            )

        clear_chat = st.button("Clear conversation")

    model_id = MODELS[model_name]

    if st.session_state.get("active_model") != model_id or clear_chat:
        st.session_state["messages"] = []
        st.session_state["active_model"] = model_id

    api_key = personal_key.strip() or configured_api_key()

    if not api_key:
        st.info(
            "Add GROQ_API_KEY to the app's Secrets, or enter your key "
            "in the sidebar to test this preview."
        )

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a study question",
        max_chars=4000,
        disabled=not bool(api_key),
        submit_mode="disable",
    )

    if question:
        question = question.strip()

        if not question:
            st.warning("Please enter a question.")
            st.stop()

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner(f"{model_name} is answering..."):
                    answer = request_answer(
                        api_key,
                        model_id,
                        st.session_state["messages"],
                        question,
                    )

            except AuthenticationError:
                st.error("The Groq API key was not accepted. Check the key.")

            except RateLimitError:
                st.warning(
                    "Groq's usage limit was reached. Please try again later."
                )

            except APITimeoutError:
                st.warning("The request timed out. Please try again.")

            except APIConnectionError:
                st.error("Could not connect to Groq. Please try again.")

            except APIError:
                st.error(
                    "Groq could not complete the request. "
                    "Try again or choose another model."
                )

            except ValueError as error:
                st.warning(str(error))

            else:
                st.markdown(answer)
                st.session_state["messages"].extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer},
                ])


if __name__ == "__main__":
    main()