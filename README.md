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
- **Subprocess**
- **dotenv**

---

## 📦 Tools Used

- `write_file` – Writes generated code to disk  
- `read_file` – Reads file content  
- `run_shell` – Executes shell commands safely  

---

## 🛠️ Installation

```bash
git clone https://github.com/hardik450/autodev-agent.git
cd autodev-agent
pip install -r requirements.txt
Create a .env file:

GOOGLE_API_KEY=your_api_key_here
▶️ Usage
Edit the task in initial_state:

"task": "Create a Python script that fetches weather data and saves it to JSON."
Run the agent:

python agent.py
The agent will:

Generate code

Execute it

Debug automatically

Stop when successful

##🖼️ Execution Screenshots


### 🔹 Planning & Code Generation
![Planner and Code Generation](https://github.com/user-attachments/assets/d611c0b9-4196-42b4-bf80-66027cf05fa6)

### 🔹 Execution & Evaluation Loop
![Execution and Evaluation](https://github.com/user-attachments/assets/656c5d18-e307-4245-ace4-66d9b71b7286)
