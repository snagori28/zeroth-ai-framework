
# Zeroth AI

Zeroth is a reasoning-first, developer-friendly AI framework designed to simulate how humans think—structured, logical, and memory-based. Unlike large language models that rely heavily on token prediction, Zeroth builds reasoning chains and stores persistent knowledge, delivering explainability, modularity, and practical intelligence.

---

## 🚀 Vision

To create AI systems that think before they speak, act with context, and reason like humans.

## 🎯 Mission

Build a lightweight, offline-friendly, explainable AI engine that is developer-first and aligns more with human cognition than probabilistic predictions.

## 💡 Core Values

- **Transparency**: Every decision is traceable.
- **Modularity**: Each agent serves a single purpose.
- **Trust-by-Design**: Human approval before saving unknowns.
- **Explainability**: Clear, human-readable reasoning.
- **Resource Efficiency**: Run where GPUs can’t.

---

## ⚙️ Features

- Modular agent architecture (Planner, Memory, Reasoner, Explainer, LLM, Ingestor)
- Dual LLM modes (Factual vs Creative), selected intelligently
- Neo4j graph-based persistent memory
- Explainable output with step-by-step inference
- Document ingestion with fact extraction and validation
- CLI and REST API interfaces
- Minimal LLM use unless necessary

---

## 📦 Installation

```bash
git clone https://github.com/snagori28/zeroth-ai-framework.git
cd zeroth-ai-framework
pip install -e .
```

---

## 🚀 Usage

### CLI Interface

```bash
python cli_interface.py
```

### REST API

```bash
uvicorn api_interface:app --reload
```

---

## 🌐 REST API Endpoints

| Endpoint         | Description                                     |
|------------------|-------------------------------------------------|
| `/plan`          | Breaks down a user goal into subtasks           |
| `/learn`         | Directly learn a new fact via user input        |
| `/ingest`        | Upload document content for auto-fact parsing   |
| `/reason`        | Uses existing memory to reason and infer        |
| `/explain`       | Returns a full explanation trace                |

---

## 📁 Project Structure

```
zeroth/
├── core/
│   ├── planner_agent.py
│   ├── memory_agent.py
│   ├── reasoner_agent.py
│   ├── explainer_agent.py
│   ├── llm_agent.py
│   └── document_ingestor.py
├── cli_interface.py
├── api_interface.py
├── config.py
├── setup.py
├── __main__.py
```

---

## 🧪 Environment Variables

```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password
export OPENAI_API_KEY=your_openai_key
```

---

## 🧠 Zeroth in Action

Example workflow:
1. Planner breaks a goal like “Plan Mars mission” into subtasks.
2. Memory checks what’s already known.
3. Reasoner makes deductions from known facts.
4. LLM is consulted *only* if something critical is missing.
5. Explainer compiles a full trace of how it reached the answer.

---

## 🔍 Real-World Use Cases

### 🧠 Business Strategy & Operations
- **Use Case**: Evaluate new market entry
- **Input**: Upload market reports and financial data
- **Outcome**: Transparent rationale based on GDP, infrastructure, and regulations

### 🏥 Medical Diagnosis
- **Use Case**: Diagnose rare symptoms
- **Input**: Upload journal articles and past patient history
- **Outcome**: Logical diagnosis trace and possible treatment paths

### 🕵️ Criminal Investigation
- **Use Case**: Pattern recognition for suspects
- **Input**: Feed police records and forensic data
- **Outcome**: Actionable suspect behavior inference

### 🎓 Education
- **Use Case**: Explain advanced physics
- **Input**: Upload lecture notes and textbooks
- **Outcome**: Simplified multi-step explanations

### 🛡️ Defense
- **Use Case**: Make tactical decisions in edge environments
- **Input**: Operate in local disconnected mode with no LLM fallback
- **Outcome**: Fast decisions on limited compute

### 🚀 Space Exploration
- **Use Case**: Simulate Mars survival protocol
- **Input**: Mission logs, technical manuals
- **Outcome**: Step-by-step guidance with no internet

## 🆚 Zeroth vs Traditional LLMs

| Feature               | Zeroth AI                         | Traditional LLMs              |
|-----------------------|-----------------------------------|-------------------------------|
| Reasoning Clarity     | Transparent reasoning chain       | Black-box answers             |
| Memory                | Structured graph memory           | Context window only           |
| Resource Requirement  | Lightweight (Neo4j, LLM fallback) | GPU-heavy                     |
| Adaptability          | High (custom docs/PDF ingestion)  | Fine-tuning needed            |
| Fact Storage          | Persistent, queryable             | Ephemeral                     |
| Explainability        | Yes (via ExplainerAgent)          | No                            |

## 🚧 Known Limitations & Forward Path

- **Scalability**: GraphDB indexing & expiration policies in development.
- **Accuracy**: Fact validation loop to enhance LLM-derived knowledge.
- **Speed**: Local cache and reduced LLM call optimization underway.

## 🌟 Why Zeroth Matters

Zeroth does not aim to replace LLMs, but to balance them. It empowers developers with tools that prioritize **clarity over guesswork**, **logic over prediction**, and **trust over magic**.

## 🔍 License

MIT License  
Author: Shrijeet Nagori  
Repo: [Zeroth AI](https://github.com/snagori28/zeroth-ai-framework)
