from core.planner_agent import PlannerAgent
from core.memory_agent import MemoryAgent
from core.reasoner_agent import ReasonerAgent
from core.llm_agent import LLM_Agent
from core.explainer_agent import ExplainerAgent
from core.document_ingestor import DocumentIngestor

def main():
    planner = PlannerAgent()
    memory = MemoryAgent()
    reasoner = ReasonerAgent()
    llm = LLM_Agent()
    explainer = ExplainerAgent()
    ingestor = DocumentIngestor(llm, memory)

    user_goal = input("Enter your goal: ").strip()
    subtasks = planner.plan(user_goal)

    explanation_trace = []
    known_facts = []

    for task in subtasks:
        fact = memory.retrieve(task)
        if not fact:
            llm_response = llm.query(task, mode="factual")
            print(f"LLM Suggested:\n{llm_response}")
            confirm = input("Store this information? (y/n): ").strip().lower()
            if confirm == 'y':
                memory.store(task, llm_response, source="llm")
                fact = llm_response
        known_facts.append(fact or "[Unknown Fact]")
        explanation_trace.append(f"Task: {task} -> Result: {fact or 'Not found'}")

    final_reasoning = reasoner.reason(known_facts)
    explanation_trace.append(f"Final Inference: {final_reasoning}")

    print("\n--- Explanation Trace ---")
    print(explainer.explain(explanation_trace))

if __name__ == '__main__':
    main()
