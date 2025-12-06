import json
from pathlib import Path
from tqdm import tqdm
from agent import ReasoningAgent

DEV_DATA = Path("data/cse476_final_project_dev_data.json")

def run_evaluation():
    if not DEV_DATA.exists():
        print(f"Error: Dev data not found at {DEV_DATA}")
        return
    with open(DEV_DATA, 'r') as f:
        dataset = json.load(f)
    agent = ReasoningAgent() # Execute agent 007 (get it? heh)
    correct_count = 0
    total_calls = 0
    test_set = dataset[:10] # Remove "[:10]" for full evaluation
    print(f"Evaluating {len(test_set)} items.")
    for item in tqdm(test_set):
        question = item["input"]
        expected = item["output"]
        result = agent.solve(question)
        prediction = result["answer"]
        is_correct = expected.strip().lower() in prediction.strip().lower() # normalization check
        if is_correct:
            correct_count += 1
        total_calls += result["calls_used"]
    accuracy = (correct_count / len(test_set)) * 100
    avg_calls = total_calls / len(test_set)
    print("\n" + "="*69)
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Avg API Calls: {avg_calls:.2f}")
    print("="*69 + "\n")

if __name__ == "__main__":
    run_evaluation()