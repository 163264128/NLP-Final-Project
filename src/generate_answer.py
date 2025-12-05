#!/usr/bin/env python3
"""
Generate a placeholder answer file that matches the expected auto-grader format.

Replace the placeholder logic inside `build_answers()` with your own agent loop
before submitting so the ``output`` fields contain your real predictions.

Reads the input questions from cse_476_final_project_test_data.json and writes
an answers JSON file where each entry contains a string under the "output" key.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
import time
from tqdm import tqdm
import os
import concurrent.futures
import threading
import sys
sys.path.append('src')
from agent import ReasoningAgent

INPUT_PATH = Path("data/cse_476_final_project_test_data.json")
OUTPUT_PATH = Path("cse_476_final_project_answers.json")

def load_questions(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    if not isinstance(data, list):
        raise ValueError("Input file must contain a list of question objects.")
    return data

write_lock = threading.Lock()
def process_single_question(args):
    """Wrapper to process a single question safely in a thread"""
    idx, question_data = args
    agent = ReasoningAgent()
    
    try:
        result = agent.solve(question_data["input"])
        answer_text = result["answer"]
    except Exception as e:
        print(f"Error on Q{idx}: {e}")
        answer_text = "Error processing"

    return {
        "idx": idx, 
        "output": answer_text
    }
def build_answers(questions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    agent = ReasoningAgent()
    answers = [None] * len(questions)
    work_items = [(i, q) for i, q in enumerate(questions, start=1)]
    MAX_WORKERS = 10 # Threading BABY!!
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_question, item): item[0] for item in work_items}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(questions), desc="Generating"):
            result = future.result()
            idx = result["idx"]
            answers[idx-1] = {"output": result["output"]}
            if idx % 100 == 0: # Checkpoint every 100 questions
                with write_lock:
                    current_valid = [a if a else {"output": ""} for a in answers]
                    with Path(f"outputs/checkpoint_{idx}.json").open("w", encoding="utf-8") as fp:
                        json.dump(current_valid, fp, ensure_ascii=False, indent=2)
        time.sleep(0.05) # Rate limiting
        answers = [a if a is not None else {"output": "Error"} for a in answers] # Preventive measure
    return answers

def validate_results(
    questions: List[Dict[str, Any]], answers: List[Dict[str, Any]]
) -> None:
    if len(questions) != len(answers):
        raise ValueError(
            f"Mismatched lengths: {len(questions)} questions vs {len(answers)} answers."
        )
    for idx, answer in enumerate(answers):
        if "output" not in answer:
            raise ValueError(f"Missing 'output' field for answer index {idx}.")
        if not isinstance(answer["output"], str):
            raise TypeError(
                f"Answer at index {idx} has non-string output: {type(answer['output'])}"
            )
        if len(answer["output"]) >= 5000:
            raise ValueError(
                f"Answer at index {idx} exceeds 5000 characters "
                f"({len(answer['output'])} chars). Please make sure your answer does not include any intermediate results."
            )

def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure output directories exist
    Path("outputs").mkdir(parents=True, exist_ok=True)
    questions = load_questions(INPUT_PATH)
    answers = build_answers(questions)

    with OUTPUT_PATH.open("w", encoding="utf-8") as fp:
        json.dump(answers, fp, ensure_ascii=False, indent=2)

    with OUTPUT_PATH.open("r", encoding="utf-8") as fp:
        saved_answers = json.load(fp)
    validate_results(questions, saved_answers)
    print(
        f"Wrote {len(answers)} answers to {OUTPUT_PATH} "
        "and validated format successfully."
    )

if __name__ == "__main__":
    main()