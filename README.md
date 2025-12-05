# CSE 476 - Final Project Instructions

**Student Name:** Sat Chidananda
**ASU ID:** 1227480945

## Project Overview
This project implements an inference-time reasoning agent designed to solve complex problems across multiple domains (Math, Coding, Common Sense, etc.). The agent uses a **multi-strategy architecture** that dynamically selects the best reasoning technique based on the complexity of the input question.

### Key Features
* **Multi-Strategy Routing:** Automatically switches between "Chain of Thought" reasoning and direct answering based on question complexity heuristics.
* **Self-Consistency:** Utilizes majority voting on multiple reasoning paths for intermediate-complexity problems to improve accuracy.
* **Robust Extraction:** Implements strict output formatting parsing to ensure answers are extracted cleanly (e.g., `Final Answer: <val>`) without reasoning chatter.
* **Parallel Processing:** The generation script utilizes multi-threading to process the large test dataset efficiently (~1.5 hours runtime).

---

## Setup & Installation

### 1. Environment Setup
Ensure you have Python 3.8+ installed. It is recommended to use a virtual environment.

# Install dependencies
`pip install -r requirements.txt`
