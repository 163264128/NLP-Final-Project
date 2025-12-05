class ChainOfThought:
    def __init__(self, api_client):
        self.api = api_client
    
    def solve_problem_with_cot(self, question: str, domain: str = None) -> str:
        system = "You are a precise reasoning agent. You generally think step-by-step but strictly follow output formats."
        prompt = f"""Problem: {question}
        Instructions:
        1. Solve the problem step-by-step.
        2. Keep your reasoning concise to ensure you do not run out of space.
        3. Your very last line MUST be exactly:
        Final Answer: <your_answer_here>
        (Do not add a period at the end of the answer)"""
        result = self.api.call_api(prompt, system=system, max_tokens=2048)
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