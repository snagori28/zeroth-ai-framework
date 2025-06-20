# Zeroth AI Framework

Zeroth is a lightweight, reasoning-first AI engine. It breaks a goal into clear subtasks, stores factual knowledge in a Neo4j graph and only calls a language model when needed. This provides explainable results and works even in limited environments.

For a deeper look at the project's philosophy and detailed use cases, see the [WHITEPAPER](WHITEPAPER.md).

## Features
- **Agent architecture** – Planner, Memory, Reasoner, Explainer, Clarifier, Feedback, LLM and DocumentIngestor
- **LLM‑first planning** – goals are broken down with an LLM and spaCy fallback
- **Dual LLM modes** – factual or creative queries depending on the task
- **Persistent graph memory** – facts are stored in Neo4j with synonym search
- **Explainable reasoning** – every step can be traced and explained to the user
- **Document ingestion** – parse text files and validate facts automatically
- **FeedbackAgent** – confirms or edits LLM‑suggested facts before saving
- **ClarifierAgent** – asks follow-up questions to refine ambiguous goals
- **CLI and REST API** – interact either from the command line or over HTTP
## Quick start
1. **Install the package** (see Installation below).
2. **Run** `python cli_interface.py` for the CLI or `uvicorn api_interface:app --reload` to start the API.
3. Provide any missing environment variables when prompted on startup.


## Installation
Clone the repository and install the package using `pip`. Installing in
standard (non-editable) mode keeps the source read-only:
```bash
git clone https://github.com/snagori28/zeroth-ai-framework.git
cd zeroth-ai-framework
pip install .
```
If you wish to hack on the framework itself, use `pip install -e .` instead.

## Usage
### Command line
Run the interactive shell. If required environment variables are not already set you will be asked for them:
```bash
python cli_interface.py
```
You will be presented with a numbered menu for planning, learning new facts and ingesting documents.
During planning the CLI may ask follow‑up questions via the ClarifierAgent. If new facts are suggested by the LLM you can accept, edit or reject them with help from the FeedbackAgent.
Respond to these prompts to refine your goal or store corrected facts. Choose "Exit" to quit.

### REST API
Start the HTTP server with:
```bash
uvicorn api_interface:app --reload
```
This exposes the endpoints described below.


### API endpoints
| Endpoint       | Description                                |
| -------------- | ------------------------------------------ |
| `/plan`        | Break a goal into subtasks                 |
| `/reason`      | Plan subtasks and produce a conclusion     |
| `/learn`       | Store a fact/value pair provided by a user |
| `/ingest`      | Ingest raw text and store extracted facts  |
| `/ingest-file` | Ingest a text file from `uploads/`         |
| `/explain`     | Return a step-by-step reasoning trace      |

## Environment variables
The CLI and API will prompt for any required values that are missing. You may also export them manually:
```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password
export OPENAI_API_KEY=your_openai_key
# Optional variables:
export UPLOAD_DIR=/path/to/uploads
export LOG_LEVEL=INFO
export MAX_UPLOAD_SIZE_MB=5
```
You can also pre-set these values in your shell if you do not want to be prompted each time.


## Running tests
```bash
pytest -q
```

## License
This project is licensed under the MIT License.
