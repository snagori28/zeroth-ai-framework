import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from core.planner_agent import PlannerAgent
from core.memory_agent import MemoryAgent
from core.reasoner_agent import ReasonerAgent
from core.llm_agent import LLM_Agent
from core.explainer_agent import ExplainerAgent
from core.document_ingestor import DocumentIngestor

logger = logging.getLogger(__name__)

app = FastAPI()
planner = PlannerAgent()
memory = MemoryAgent()
reasoner = ReasonerAgent()
llm = LLM_Agent()
explainer = ExplainerAgent()
ingestor = DocumentIngestor(llm, memory)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down MemoryAgent")
    memory.close()

class TaskRequest(BaseModel):
    """Request body for endpoints that require a goal."""

    goal: str

class LearnRequest(BaseModel):
    """Request body for storing a user-provided fact."""

    fact: str
    value: str

class IngestRequest(BaseModel):
    """Request body for direct text ingestion."""

    content: str

class IngestFileRequest(BaseModel):
    """Request body for ingesting a file from ``uploads`` directory."""

    filename: str  # Name of a text file located in Config.UPLOAD_DIR

@app.post("/plan")
def plan(req: TaskRequest):
    """Return a simple plan for the given goal."""

    logger.info("/plan called with goal: %s", req.goal)
    return {"subtasks": planner.plan(req.goal)}

@app.post("/reason")
def reason(req: TaskRequest):
    """Plan subtasks and combine them into a reasoning result."""

    logger.info("/reason called with goal: %s", req.goal)
    subtasks = planner.plan(req.goal)
    known_facts = [memory.retrieve(task) or "[Unknown Fact]" for task in subtasks]
    result = reasoner.reason(known_facts)
    return {"reasoning": result}

@app.post("/learn")
def learn(req: LearnRequest):
    """Store a fact-value pair supplied by the user."""

    logger.info("/learn storing fact '%s'", req.fact)
    memory.store(req.fact, req.value, source="user")
    return {"status": "stored", "fact": req.fact}

@app.post("/ingest")
def ingest(req: IngestRequest):
    """Ingest raw text and store any discovered facts."""

    logger.info("/ingest called")
    ingestor.ingest(req.content)
    return {"status": "ingested"}

@app.post("/ingest-file")
def ingest_file(req: IngestFileRequest):
    """Load a text file from ``uploads`` and ingest its contents."""

    filepath = os.path.join("uploads", req.filename)
    logger.info("/ingest-file loading %s", filepath)
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    ingestor.ingest(content)
    return {"status": "file ingested", "filename": req.filename}

@app.post("/explain")
def explain(req: TaskRequest):
    """Provide an explanation of the reasoning process for a goal."""

    logger.info("/explain called with goal: %s", req.goal)
    subtasks = planner.plan(req.goal)
    known_facts = [memory.retrieve(task) or "[Unknown Fact]" for task in subtasks]
    reasoning = reasoner.reason(known_facts)
    steps = [f"Task: {task} -> Result: {fact}" for task, fact in zip(subtasks, known_facts)]
    steps.append(f"Final Inference: {reasoning}")
    return {"explanation": explainer.explain(steps)}
