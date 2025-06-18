import os
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

    explanation_trace = []

    while True:
        print("\n=== Zeroth CLI ===")
        print("1. Plan & Reason a Goal")
        print("2. Learn a Fact Manually")
        print("3. Ingest a Document")
        print("4. Query Memory")
        print("5. Explain Last Output")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            user_goal = input("Enter your goal: ").strip()
            subtasks = planner.plan(user_goal)
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

        elif choice == '2':
            fact = input("Enter fact name: ").strip()
            value = input("Enter fact value: ").strip()
            memory.store(fact, value, source="user")
            print("Fact stored successfully.")

        elif choice == '3':
            print("Choose document ingestion method:")
            print("1. Paste manually")
            print("2. Upload from file (in ./uploads)")
            doc_option = input("Select (1 or 2): ").strip()

            if doc_option == '2':
                filename = input("Enter filename (from ./uploads): ").strip()
                filepath = os.path.join("uploads", filename)
                if not os.path.exists(filepath):
                    print("File not found.")
                    continue
                with open(filepath, 'r', encoding='utf-8') as file:
                    document_content = file.read()
            else:
                print("Paste your document content below. Type 'END' on a new line to finish:")
                lines = []
                while True:
                    line = input()
                    if line.strip().upper() == 'END':
                        break
                    lines.append(line)
                document_content = "\n".join(lines)

            ingestor.ingest(document_content)
            print("Document processed and facts stored.")

        elif choice == '4':
            query = input("Enter fact name to query: ").strip()
            result = memory.retrieve(query)
            print(f"Fact: {result or '[Not Found]'}")

        elif choice == '5':
            if explanation_trace:
                print("\n--- Last Explanation ---")
                print(explainer.explain(explanation_trace))
            else:
                print("No previous explanation found.")

        elif choice == '6':
            print("Exiting Zeroth CLI. Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
