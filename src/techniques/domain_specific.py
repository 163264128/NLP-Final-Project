class DomainSpecificSolver:
    def __init__(self, api_client):
        self.api = api_client
        self.domain_prompts = {
            "math": "You are a mathematics expert who prefers numerical proofs. Solve step by step and show your work.",
            "coding": "You are an expert programmer who tackles complex code with helper functions. Write clean, error-free and accurate code.",
            "common_sense": "You are knowledgeable about general facts. Answer concisely.",
            "planning": "You are a planning guru. Think through the sequence of actions.",
            "future_prediction": "You are an expert analyst. Make informed predictions based on patterns."
        }
    
    def solve_with_domain_specific_prompt(self, question: str, domain: str = None) -> str:
        system = self.domain_prompts.get(domain, "You are a helpful and pragmatic assistant.")
        # Domain-specific formatting
        if domain == "math":
            prompt = f"Solve this math problem:\n\n{question}\n\nFinal Answer:"
        elif domain == "coding":
            prompt = f"Write code for:\n\n{question}\n\nCode:"
        else:
            prompt = f"{question}\n\nAnswer:"
        result = self.api.call(prompt, system=system, max_tokens=256)
        if not result["ok"]:
            return None 
        return result["text"].strip()