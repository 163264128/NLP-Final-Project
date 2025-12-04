class ChainOfThought:
    def __init__(self, api_client):
        self.api = api_client
    
    def solve_problem_with_cot(self, question: str, domain: str = None) -> str:
        system = "You are an expert problem solver. Think step by step."
        prompt = f"""Solve this problem step by step:
        {question}
        Think through your reasoning carefully, then provide the final answer at the end."""
        result = self.api.call_api(prompt, system=system, max_tokens=1024)
        if not result["ok"]:
            return None
        response = result["text"] 
        return self.extract_answer(response) 
    
    def extract_answer(self, text: str) -> str: # Extract final answer
        if "Final Answer:" in text: # More sophisticated extraction
            parts = text.split("Final Answer:")
            answer = parts[-1].strip()
            answer = answer.split('\n')[0].strip()  # Take first line after "Final Answer:"
            return answer
        lines = text.strip().split('\n') # Bare bones extraction -> THE OG. 
        for line in reversed(lines):
            if line.strip():
                return line.strip()
        return text.strip()