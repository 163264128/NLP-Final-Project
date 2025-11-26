class SelfConsistency:
    def __init__(self, api_client, num_samples=3):
        self.api = api_client
        self.num_samples = num_samples
    
    def solve_problem_with_self_consistency(self, question: str, domain: str = None) -> str:
        answers = []
        system = "You are an expert problem solver."
        prompt = f"Solve: {question}\n\nProvide only the final answer."
        for _ in range(self.num_samples): # Samples with temperature > 0
            result = self.api.call(prompt, system=system, temperature=0.7)
            if result["ok"]:
                answers.append(result["text"].strip())
        if not answers:
            return None