# AutoDev-Agent 🤖⚙️

An autonomous coding assistant built using **LangGraph** that can plan tasks, write code, execute it, evaluate results, and iteratively fix errors until task requirements are satisfied.

This project demonstrates **multi-step autonomous reasoning**, **tool use**, **human-in-the-loop clarification**, and **stateful execution loops**, inspired by systems like Devin.

---

## 🚀 Features

- 🧠 **Task Planning** – Breaks down a natural language task into actionable steps
- ❓ **Human Clarification** – Asks the user for missing inputs before writing any code
- ✍️ **Autonomous Code Generation** – Writes complete executable code
- 🗂️ **Dynamic File Handling** – Chooses filenames automatically
- ▶️ **Code Execution** – Runs generated code in the local environment
- 🔁 **Self-Correction Loop** – Fixes errors based on execution output
- ✅ **Task Evaluation** – Stops only when task objectives are satisfied
- 🧩 **LangGraph-Based Workflow** – Explicit state transitions and control flow

---

## 🏗️ Architecture

AutoDev-Agent is implemented as a **stateful graph** using LangGraph.

### Agent Roles (Logical Agents)

| Node       | Responsibility                                              |
|------------|-------------------------------------------------------------|
| Clarifier  | Detects missing inputs and asks the user before planning    |
| Planner    | Converts task + clarifications → step-by-step plan         |
| Coder      | Writes full code and selects filename                       |
| Executor   | Saves and runs code                                         |
| Fixer      | Debug-fixes code if execution fails                         |
| Evaluator  | Verifies task completion                                    |
| Controller | Decides loop or termination                                 |

> Though implemented in a single graph, each node behaves as an independent **logical agent**.

---

## 🔄 Workflow

```
Task
↓
Clarifier ── (asks user if inputs are missing)
↓
Planner
↓
Coder
↓
Executor
↓
Evaluator ── SUCCESS → END
│
└─ FAILURE → Fixer → Executor (loop)
```

---

## ❓ Clarifier Node

Before any planning or code generation begins, the **Clarifier** node analyses the task and determines whether any information is missing that the agent cannot reasonably infer on its own.

### How it works

1. The task is sent to the LLM with only the `human_input` tool available.
2. The LLM decides: is this task fully self-contained, or are there gaps?
3. If gaps exist, it calls `human_input` once per missing piece of information.
4. The user's answers are appended to the task context.
5. Every downstream node (Planner, Coder, etc.) sees the enriched task automatically.

### Example

```
Task: "Build a web scraper and save results to a file."

🤖 Agent needs clarification: What URL should be scraped?
Your answer: https://quotes.toscrape.com

🤖 Agent needs clarification: What data should be extracted from the page?
Your answer: All quote text and author names

🤖 Agent needs clarification: What format should the output file be in — CSV or JSON?
Your answer: JSON
```

The Planner then receives:

```
Build a web scraper and save results to a file.

User clarifications:
- Q: What URL should be scraped?
  A: https://quotes.toscrape.com
- Q: What data should be extracted from the page?
  A: All quote text and author names
- Q: What format should the output file be in — CSV or JSON?
  A: JSON
```

### When clarification is skipped

If the task is fully self-contained (e.g. *"Fetch the machine's IP address and save it to ip_address.txt"*), the Clarifier replies `NO_CLARIFICATION_NEEDED` and the agent proceeds directly to planning with zero interruption.

---

## 🧠 Tech Stack

- **Python**
- **LangGraph**
- **LangChain**
- **Google Gemini (via LangChain)**
- **Subprocess**
- **dotenv**

---

## 📦 Tools Used

| Tool          | Purpose                                              |
|---------------|------------------------------------------------------|
| `human_input` | Asks the user a clarifying question during setup     |
| `write_file`  | Writes generated code to disk                        |
| `read_file`   | Reads file content                                   |
| `run_shell`   | Executes shell commands safely                       |

---

## 🛠️ Installation

```bash
git clone https://github.com/hardik450/autodev-agent.git
cd autodev-agent
pip install -r requirements.txt
```

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Usage

Edit the task in `initial_state`:

```python
"task": "Create a Python script that fetches weather data and saves it to JSON."
```

Run the agent:

```bash
python agent.py
```

The agent will:

1. Ask clarifying questions if any inputs are missing
2. Generate a plan using your answers
3. Write and execute the code
4. Debug automatically if errors occur
5. Stop when the task is successfully completed

---

<img width="901" height="635" alt="Screenshot 2026-01-31 102447" src="https://github.com/user-attachments/assets/3fe6a8f8-ddd9-4de8-811d-d8232ce33ff0" />
<img width="858" height="657" alt="Screenshot 2026-01-31 102501" src="https://github.com/user-attachments/assets/50955b2a-dde5-4d27-9877-4b119e7b1989" />
