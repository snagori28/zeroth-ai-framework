# Zeroth AI Whitepaper

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
## ⚙️ Key Features
- Modular agent architecture (Planner, Memory, Reasoner, Explainer, Clarifier, Feedback, LLM and Ingestor)
- LLM-first planning with spaCy fallback
- Dual LLM modes for factual or creative reasoning
- Graph memory with synonym search and fuzzy matching
- Document ingestion with fact validation
- Chain-of-thought reasoning traces
- Works offline with minimal LLM use

## 🧠 Zeroth in Action

### Planner Agent
Decomposes high‑level goals into clear subtasks.
*Real-life analogy*: like a mission commander breaking “Plan Mars Mission” into
`["Check life support", "Assess gravity", "Find food sources"]`.

### Clarifier Agent
Poses short follow-up questions when a subtask is vague.
Example: for "Check life support" it might ask "How many crew members are on board?" to clarify the requirement.

### Memory Agent (Neo4j)
Persistent, queryable knowledge graph that stores and retrieves structured
facts. Acts as long‑term memory.
Example stored fact: `life_support → "Oxygen tanks last 14 days"`.

### LLM Agent
Used only when the memory has a gap.
Dual mode:
- **Factual** – extract concise, bulleted facts. Example prompt: "Give bullet
  points for how gravity affects muscle loss".
- **Creative** – freeform generative output when more narrative is required.

### Reasoner Agent
Combines known facts to form logical inferences—think deductive reasoning.
Example: input `["Oxygen lasts 14 days", "Trip will take 20 days"]` → output
`Insufficient oxygen for mission`.

### Feedback Agent
Validates new facts before they are stored. Example: if the LLM suggests
`"Oxgen can by sythesised on mars"`, the agent decides to accept, edit or reject it before
adding to memory.

### Explainer Agent
Builds transparent reasoning traces.

Example trace:
1. Task: Assess oxygen supply
2. Memory: Oxygen lasts 14 days
3. Memory: Trip will take 20 days
4. Inference: We will need more oxygen supply for the mission to be safe.

### Document Ingestor
Uses the LLM in factual mode to ingest files and extract structured facts.
Example: uploading a Martian soil PDF yields
`{"Soil Type": "Basaltic", "Water Content": "2%"}`.

Together these agents form a loop: the Planner sets subtasks, the Clarifier
asks for missing details, Memory recalls facts, the LLM fills knowledge gaps,
the Reasoner deduces new insights, the Feedback agent vets new facts, the
Explainer narrates the steps, and the Document Ingestor expands the knowledge
base.

---

## 🔍 Real-World Use Cases

### 🧠 Business Strategy & Operations
- **Use Case**: Evaluate new market entry
- **Input**: Upload market reports and financial data
- **Outcome**: Rational decision based on GDP, infrastructure, and regulations

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
