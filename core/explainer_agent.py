class ExplainerAgent:
    def explain(self, steps):
        return "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
