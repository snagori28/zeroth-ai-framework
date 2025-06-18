import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from core.planner_agent import PlannerAgent
from core.memory_agent import MemoryAgent
from core.reasoner_agent import ReasonerAgent
from core.llm_agent import LLM_Agent
from core.explainer_agent import ExplainerAgent
from core.document_ingestor import DocumentIngestor

app = FastAPI()
planner = PlannerAgent()
memory = MemoryAgent()
reasoner = ReasonerAgent()
llm = LLM_Agent()
explainer = ExplainerAgent()
ingestor = DocumentIngestor(llm, memory)

class TaskRequest(BaseModel):
    goal: str

class LearnRequest(BaseModel):
    fact: str
    value: str

class IngestRequest(BaseModel):
    content: str

class IngestFileRequest(BaseModel):
    filename: str  # Name of a text file located in Config.UPLOAD_DIR

@app.post("/plan")
def plan(req: TaskRequest):
    return {"subtasks": planner.plan(req.goal)}

@app.post("/reason")
def reason(req: TaskRequest):
    subtasks = planner.plan(req.goal)
    known_facts = [memory.retrieve(task) or "[Unknown Fact]" for task in subtasks]
    result = reasoner.reason(known_facts)
    return {"reasoning": result}

@app.post("/learn")
def learn(req: LearnRequest):
    memory.store(req.fact, req.value, source="user")
    return {"status": "stored", "fact": req.fact}

@app.post("/ingest")
def ingest(req: IngestRequest):
    ingestor.ingest(req.content)
    return {"status": "ingested"}

@app.post("/ingest-file")
def ingest_file(req: IngestFileRequest):
    filepath = os.path.join("uploads", req.filename)
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    ingestor.ingest(content)
    return {"status": "file ingested", "filename": req.filename}

@app.post("/explain")
def explain(req: TaskRequest):
    subtasks = planner.plan(req.goal)
    known_facts = [memory.retrieve(task) or "[Unknown Fact]" for task in subtasks]
    reasoning = reasoner.reason(known_facts)
    steps = [f"Task: {task} -> Result: {fact}" for task, fact in zip(subtasks, known_facts)]
    steps.append(f"Final Inference: {reasoning}")
    return {"explanation": explainer.explain(steps)}
