import json
from api_client import ModelAPI
from techniques.cot import ChainOfThought
from techniques.self_consistency import SelfConsistency
from techniques.direct_solver import DirectSolver

class ReasoningAgent:
    def __init__(self):
        self.api = ModelAPI()
        self.cot = ChainOfThought(self.api)
        self.consistency = SelfConsistency(self.api, num_samples=3)
        self.direct = DirectSolver(self.api)
    
    def solve(self, question: str, domain: str = None) -> dict:
        self.api.reset_count()
    # Flow : Direct -> CoT -> Self-Consistency -> Direct  
        is_complex = self.is_question_complex(question) # Complex questions -> CoT + Self Consistency
        if is_complex:
            answer = self.cot.solve_problem_with_cot(question, domain)
        elif self.api.call_count < 8:
            answer = self.consistency.solve_problem_with_self_consistency(question, domain)
        else:
            answer = self.direct.solve_problem_with_direct_prompting(question, domain)
        if not answer: # No Answer from CoT + Self Consistency -> Try Direct Prompt Solver
            answer = self.direct.solve_problem_with_direct_prompting(question, domain)
        if answer:
            answer = self.clean_formatting(answer) # Remove weird formatting
        return {"answer": answer or "Can't Solve",
                "calls_used": self.api.call_count,
                "domain": domain}

    def is_question_complex(self, question: str) -> bool:
        if any(word in question.lower() for word in ['solve', 'calculate', 'prove', 'find the area', 'compute']):
            return True # Common Math terms
        if len(question) > 500:
            return True # Lengthy questions
        if any(word in question.lower() for word in ['first', 'then', 'finally', 'step by step']):
            return True # Premise-Connected questions
        return False
    
    def clean_formatting(self, answer: str) -> str:
        if not answer: return answer # Answer not generated 
        answer = answer.replace('**', '').replace('*', '') # Remove any markdown formatting
        if answer.startswith('"') and answer.endswith('"'): # Remove double quotes
            answer = answer[1:-1]
        if answer.startswith("'") and answer.endswith("'"): # Remove single quotes
            answer = answer[1:-1]
        if len(answer) > 4000:  # Truncate with crucial stuff if answer too long
            answer = answer[:4000].rsplit('.', 1)[0] + '.'
        return answer.strip()