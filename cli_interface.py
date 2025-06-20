import os
from core.planner_agent import PlannerAgent
from core.memory_agent import MemoryAgent
from core.reasoner_agent import ReasonerAgent
from core.llm_agent import LLM_Agent
from core.explainer_agent import ExplainerAgent
from core.document_ingestor import DocumentIngestor
from core.feedback_agent import FeedbackAgent
from core.clarifier_agent import ClarifierAgent
from config import Config, ensure_env_vars

def main():
    """Launch the interactive command line interface."""

    # Ask for any configuration values that are not provided via environment.
    ensure_env_vars()

    planner = PlannerAgent()
    memory = MemoryAgent()
    llm = LLM_Agent()
    feedback = FeedbackAgent(llm)
    clarifier = ClarifierAgent(llm_agent=llm)
    reasoner = ReasonerAgent(llm_agent=llm)
    explainer = ExplainerAgent(llm_agent=llm)
    ingestor = DocumentIngestor(llm, memory, feedback)

    explanation_trace = []

    try:
        while True:
            print("\n=== Zeroth CLI ===")
            print("1. Plan & Reason a Goal")
            print("2. Clarify a Goal")
            print("3. Learn a Fact Manually")
            print("4. Ingest a Document")
            print("5. Query Memory")
            print("6. Explain Last Output")
            print("7. Exit")

            choice = input("Select an option (1-7): ").strip()

            if choice == '1':
                # Reset explanation trace for each new reasoning cycle
                explanation_trace = []
                user_goal = input("Enter your goal: ").strip()
                follow_ups = clarifier.clarify(user_goal)
                for q in follow_ups:
                    ans = input(f"{q} ").strip()
                    if ans:
                        user_goal += f"\n{q}: {ans}"
                subtasks = planner.plan(user_goal)
                known_facts = []

                for task in subtasks:
                    fact = memory.retrieve(task)
                    if not fact:
                        llm_response = llm.query(task, mode="factual")
                        print(f"LLM Suggested:\n{llm_response}")
                        suggested = feedback.review(task, llm_response)
                        print(f"LLM suggests to {suggested} this fact.")
                        user_choice = input("Accept, edit, or reject? (a/e/r): ").strip().lower()
                        decision = user_choice[0] if user_choice else suggested[0]
                        if decision == 'r':
                            fact = None
                        elif decision == 'e':
                            fact, llm_response = feedback.edit(task, llm_response)
                            memory.store(fact, llm_response, source="llm")
                            fact = llm_response
                        else:
                            memory.store(task, llm_response, source="llm")
                            fact = llm_response
                    known_facts.append(fact or "[Unknown Fact]")
                    explanation_trace.append(f"Task: {task} -> Result: {fact or 'Not found'}")

                final_reasoning = reasoner.reason(known_facts)
                explanation_trace.append(f"Final Inference: {final_reasoning}")
                print("\n--- Explanation Trace ---")
                print(explainer.explain(explanation_trace))

            elif choice == '2':
                user_goal = input("Enter your goal: ").strip()
                questions = clarifier.clarify(user_goal)
                if questions:
                    print("\nClarifying questions:")
                    for q in questions:
                        print(f"- {q}")
                else:
                    print("No clarification needed.")

            elif choice == '3':
                fact = input("Enter fact name: ").strip()
                value = input("Enter fact value: ").strip()
                memory.store(fact, value, source="user")
                print("Fact stored successfully.")

            elif choice == '4':
                print("Choose document ingestion method:")
                print("1. Paste manually")
                print(f"2. Upload from file (in {Config.UPLOAD_DIR})")
                doc_option = input("Select (1 or 2): ").strip()

                if doc_option == '2':
                    filename = input(f"Enter filename (from {Config.UPLOAD_DIR}): ").strip()
                    base_dir = os.path.abspath(Config.UPLOAD_DIR)
                    filepath = os.path.abspath(os.path.join(base_dir, filename))
                    if not filepath.startswith(base_dir + os.sep):
                        print("Invalid file path.")
                        continue
                    if not os.path.exists(filepath):
                        print("File not found.")
                        continue
                    ingestor.ingest(filepath)
                else:
                    print("Paste your document content below. Type 'END' on a new line to finish:")
                    lines = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'END':
                            break
                        lines.append(line)
                    content = "\n".join(lines)
                    ingestor.ingest(content)

                print("Document processed and facts stored.")

            elif choice == '5':
                query = input("Enter fact name to query: ").strip()
                result = memory.retrieve(query)
                print(f"Fact: {result or '[Not Found]'}")

            elif choice == '6':
                if explanation_trace:
                    print("\n--- Last Explanation ---")
                    print(explainer.explain(explanation_trace))
                else:
                    print("No previous explanation found.")

            elif choice == '7':
                print("Exiting Zeroth CLI. Goodbye!")
                break

            else:
                print("Invalid option. Try again.")

    finally:
        memory.close()

if __name__ == '__main__':
    main()
