# AutoDev-Agent 🤖⚙️

An autonomous coding assistant built using **LangGraph** that can plan tasks, write code, execute it, evaluate results, and iteratively fix errors until task requirements are satisfied.

This project demonstrates **multi-step autonomous reasoning**, **tool use**, and **stateful execution loops**, inspired by systems like Devin.

---

## 🚀 Features

- 🧠 **Task Planning** – Breaks down a natural language task into actionable steps
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

| Node        | Responsibility |
|------------|---------------|
| Planner     | Converts task → step-by-step plan |
| Coder       | Writes full code and selects filename |
| Executor    | Saves and runs code |
| Fixer       | Debug-fixes code if execution fails |
| Evaluator   | Verifies task completion |
| Controller  | Decides loop or termination |

> Though implemented in a single graph, each node behaves as an independent **logical agent**.

---

## 🔄 Workflow

Task
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


---

## 🧠 Tech Stack

- **Python**
- **LangGraph**
- **LangChain**
- **Google Gemini (via LangChain)**
- **Subprocess (for execution)**
- **dotenv**

---

## 📦 Tools Used

- `write_file` – Writes generated code to disk
- `read_file` – Reads file content
- `run_shell` – Executes shell commands safely

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/autodev-agent.git
cd autodev-agent
pip install -r requirements.txt
Create a .env file:

GOOGLE_API_KEY=your_api_key_here
▶️ Usage
Edit the task in initial_state:

"task": "Create a Python script that fetches weather data and saves it to JSON."
Run:

python agent.py
The agent will:

generate code

run it

debug automatically

stop when successful


<img width="858" height="657" alt="Screenshot 2026-01-31 102501" src="https://github.com/user-attachments/assets/d611c0b9-4196-42b4-bf80-66027cf05fa6" />
<img width="901" height="635" alt="Screenshot 2026-01-31 102447" src="https://github.com/user-attachments/assets/656c5d18-e307-4245-ace4-66d9b71b7286" />

