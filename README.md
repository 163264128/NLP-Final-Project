# CSE 476 - Final Project Instructions

**Student Name:** Sat Chidananda

## Project Overview
This project implements an inference-time reasoning agent designed to solve complex problems across multiple domains (Math, Coding, Common Sense, etc.). The agent uses a **multi-strategy architecture** that dynamically selects the best reasoning technique based on the complexity of the input question.

### Key Features
* **Multi-Strategy Routing:** Automatically switches between "Chain of Thought" reasoning and direct answering based on question complexity heuristics.
* **Self-Consistency:** Utilizes majority voting on multiple reasoning paths for intermediate-complexity problems to improve accuracy.
* **Robust Extraction:** Implements strict output formatting parsing to ensure answers are extracted cleanly (e.g., `Final Answer: <val>`) without reasoning chatter.
* **Parallel Processing:** The generation script utilizes multi-threading to process the large test dataset efficiently (~1 hour runtime).

---

## Grader Instructions (Evaluation)

To verify the agent's performance on the development set, please follow these steps:

### Prerequisites
* Ensure you are connected to the **ASU Network** or **VPN** (Required for API access).
* Python 3.8+ is installed.
* Clone the repo: `git clone https://github.com/163264128/NLP-Final-Project.git`
* Be in root directory:  `cd NLP-Final-Project`
  
### Setup
#### Install core dependencies
`pip install -r requirements.txt`

### Configure Environment Variables 
#### Create a .env file in the root directory with the following lines:
`OPENAI_API_KEY=cse476`\
`API_BASE=http://10.4.58.53:41701/v1`\
`MODEL_NAME=bens_model`

### Verify
Run `python src/evaluate.py`

### Generate Answers to Reproduce 
Run `python src/generate_answer.py`
