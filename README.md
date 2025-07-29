# Local Assistant

Local assistant, Mike, is an AI assistant chatbot designed to run in your personal PC.
Mike can help you to increase your productivity without any risk on your privacy.

## Installation

Local assistant supports both Ollama (for local models) and Groq (for cloud-hosted models). You can choose which provider to use in the configuration. For tracing and collecting usage data, you can use either LangSmith or Langfuse.

If you want to use Ollama, you need to install it and download a language model. If you want to use Groq, you need to provide your Groq API key in the .env file.


### Ollama Installation (Optional)

Go to [Ollama Home Page](https://ollama.com/). Choose your platform to install and follow the instructions.

Download a language model (e.g., Llama3):

```bash
ollama pull llama3
```

Please note that language models run best on GPUs. If you do not have a GPU you can still use a language model, but it will be slow. A typical language model will require approximately 5GB of disk space.

For a list of available models, see [Ollama Models Library](https://ollama.com/library).

### Groq Setup (Optional)

To use Groq models, sign up at [Groq Cloud](https://console.groq.com/) and obtain your API key. Add your API key to the configuration file as described below.

### Python Installation

Go to [Official Python Downloads Page](https://www.python.org/downloads/).

### Installing Local Assistant

Use install scripts provided for your platform e.g. windows, linux.

For linux environment you may need to give execute permission to the scripts.

```bash
chmod +x install-linux.sh
```


### Configuration

The configuration file is `config/config.yml`. Edit it to configure options like model provider (Ollama or Groq), API keys, database, and tracing (LangSmith or Langfuse).

To enable tracing, set the appropriate options for LangSmith or Langfuse in the configuration file.

Prompts are in the `config/prompts.yml` file. You may edit this file to provide your own prompts.

### Launching Local Assistant

Use launch script provided for your platform e.g. windows, linux.

For linux environment you may need to give execute permission to the scripts.

```bash
chmod +x launch-linux.sh
```

## Using Local Assistant

Open chat screen at [Assistant Chat](http://localhost:8501/Assistant_Chat).

## Sample .env file

`.env` file is used to specify environment variables to the application. Especially sensitive information like api keys. Here is a sample file content:

```text
GROQ_API_KEY=<dummy-text>
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<dummy-text>
LANGSMITH_PROJECT=groq-demo-project
LANGFUSE_SECRET_KEY=<dummy-text>
LANGFUSE_PUBLIC_KEY=<dummy-text>
LANGFUSE_HOST=http://localhost:3000
```
> Note that you do not need to provide langsmith or langfuse variables. Populate any of them if you want to use.

## Provide Feedback

If you encounter an issue, feel free to report it by opening a GitHub issue.

