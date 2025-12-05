from collections import Counter

class SelfConsistency:
    def __init__(self, api_client, num_samples=3):
        self.api = api_client
        self.num_samples = num_samples
    
    def solve_problem_with_self_consistency(self, question: str, domain: str = None) -> str:
        candidate_answers = []
        system = "You are a precise solver. You output ONLY the result. No labels. No punctuation."
        prompt = f"""Question: {question}
                Instructions:
                - Output ONLY the final answer (e.g., "5" or "Paris").
                - Do NOT write "Answer:", "The answer is", or add a period.
                - Do NOT provide any reasoning or explanation."""
        for _ in range(self.num_samples): # Samples with temperature > 0
            result = self.api.call_api(prompt, system=system, temperature=0.7, max_tokens=512)
            if result["ok"]:
                candidate_answers.append(result["text"].strip())
        if not candidate_answers:
            return None
        vote_counts = Counter(candidate_answers)
        max_votes = 0
        for answer, count in vote_counts.items(): # Find the highest number of votes any answer received
            if count > max_votes:
                max_votes = count
        top_candidates = []
        for answer, count in vote_counts.items():
            if count == max_votes: # Candidates tied in top spot
                top_candidates.append(answer)
        best_answer = top_candidates[0]
        for candidate in top_candidates:
            if len(candidate) > len(best_answer): # Among tied candidates, choose the longest one
                best_answer = candidate
        return best_answer