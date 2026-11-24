# Research and Study Assistant — Without RAG

A study chatbot built with Streamlit and Groq. This teaching demonstration lets users select an LLM, ask questions, and explore follow-up conversations.

**[Open the live app](https://llm-study-assistant-without-rag.streamlit.app/)**

## Purpose

This project demonstrates an LLM application without retrieval-augmented generation (RAG).

Responses use the selected model's learned knowledge and recent conversation. The app does not upload PDFs, search documents, or browse the web.

It provides a foundation for understanding the separate **Research and Study Assistant** project, which adds PDF upload and document retrieval.

## Features

- Choose between three LLMs hosted by Groq.
- Ask study questions and follow-up questions.
- View conversation history during the current session.
- Clear the conversation at any time.
- Start a fresh conversation when changing models.
- Use the app's configured Groq access or optionally supply your own Groq API key.

## Available models

| Display name | Groq model ID |
|---|---|
| GPT-OSS 120B | `openai/gpt-oss-120b` |
| GPT-OSS 20B | `openai/gpt-oss-20b` |
| Qwen 3.8 27B | `qwen/qwen3.8-27b` |

## Using the app

1. Open the live app.
2. Select a model from the sidebar.
3. Enter a study question.
4. Ask follow-up questions or clear the conversation.
5. To compare models, select another model and repeat the same question.

Example questions:

- Explain overfitting with a simple example.
- What is the difference between classification and regression?
- Explain retrieval-augmented generation in plain language.

## Groq API access

The deployed app can use a Groq API key configured by its owner in Streamlit Secrets.

The optional sidebar field lets users supply their own Groq key for their session. Leave it blank to use the app's configured access.

**Only Groq API keys are supported.** Keys from OpenAI, Google Gemini, or Anthropic cannot be used with the current implementation.

For your own deployment, add the following under the app's Streamlit Secrets settings:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

Keep actual API keys out of source files, this README, and GitHub commits.

## Running in Codespaces or locally

Open the project folder and ensure [uv](https://docs.astral.sh/uv/getting-started/installation/) is installed.

Install the project dependencies:

```bash
uv sync
```

Start the app:

```bash
uv run streamlit run streamlit_app.py
```

In Codespaces, open forwarded port **8501** from the Ports panel. On your computer, open the local URL shown in the terminal.

If the preview has no configured key, enter a Groq key in the optional sidebar field. The app also supports the `GROQ_API_KEY` environment variable.

Keys saved in Streamlit Community Cloud are configured separately from the Codespaces preview.

## Project files

| File | Purpose |
|---|---|
| `streamlit_app.py` | App interface, conversation state, and Groq requests |
| `pyproject.toml` | Project configuration and dependencies |
| `uv.lock` | Locked dependency versions |
| `.python-version` | Python version selection for development |
| `README.md` | Project overview and setup instructions |

## Publishing updates

Changes saved in Codespaces appear in its preview. To update the deployed Streamlit app, commit and push the changes to GitHub.

Streamlit Community Cloud then updates the app from its connected repository.

## Difference from the RAG solution

| Capability | This demonstration | RAG solution |
|---|---|---|
| Three Groq model choices | Yes | Yes |
| PDF upload | No | Up to 50 PDFs |
| Retrieval of document passages | No | Yes |
| Answers based on retrieved PDF passages | No | Yes |


## Limitations

- Answers may contain inaccuracies and should be checked against reliable sources.
- The app does not retrieve evidence or verify references.
- Conversation history is temporary and is not saved in a database.
- Model availability and API usage limits depend on Groq.

## Documentation

- [Streamlit documentation](https://docs.streamlit.io/)
- [Groq documentation](https://console.groq.com/docs/)
- [uv documentation](https://docs.astral.sh/uv/)