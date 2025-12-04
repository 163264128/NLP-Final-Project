class DirectSolver:
    def __init__(self, api_client):
        self.api = api_client
    
    def solve_problem_with_direct_prompting(self, question: str, domain: str = None) -> str:
        system = "You are a helpful assistant. Provide concise, accurate answers."
        prompt = f"""{question}
        Provide only the final answer. Be concise."""
        result = self.api.call_api(prompt, system=system, max_tokens=256)
        if not result["ok"]:
            return None 
        return result["text"].strip()