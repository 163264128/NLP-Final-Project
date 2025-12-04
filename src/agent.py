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