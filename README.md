# Zeroth AI Framework

Zeroth is a lightweight, reasoning-first AI engine. It breaks a goal into clear subtasks, stores factual knowledge in a Neo4j graph and only calls a language model when needed. This provides explainable results and works even in limited environments.

For a deeper look at the project's philosophy and detailed use cases, see the [WHITEPAPER](WHITEPAPER.md).

## Features
- **Agent architecture** – Planner, Memory, Reasoner, Explainer, LLM and DocumentIngestor
- **Dual LLM modes** – factual or creative queries depending on the task
- **Persistent graph memory** – facts are stored in Neo4j for later retrieval
- **Explainable reasoning** – every step can be traced and explained to the user
- **CLI and REST API** – interact either from the command line or over HTTP
- **Document ingestion** – parse text files and extract facts automatically

## Installation
```bash
git clone https://github.com/snagori28/zeroth-ai-framework.git
cd zeroth-ai-framework
pip install -e .
```

## Usage
### Command line
```bash
python cli_interface.py
```

### REST API
```bash
uvicorn api_interface:app --reload
```

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
Set these variables before running Zeroth:
```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password
export OPENAI_API_KEY=your_openai_key
```

## Running tests
```bash
pytest -q
```

## License
This project is licensed under the MIT License.
