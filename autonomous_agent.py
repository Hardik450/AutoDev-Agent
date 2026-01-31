from dotenv import load_dotenv
import os
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import subprocess
import operator
from langchain_core.messages import AnyMessage, SystemMessage
load_dotenv()

@tool
def write_file(file_path: str, content: str) -> str:
    """It writes content to the file"""
    with open(file_path, 'w') as file:
        file.write(content)
    return f"File created at {file_path}"
    
@tool
def read_file(file_path: str) -> str:
    """It reads the file content"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return f"Error: File {file_path} does not exist."
    
@tool
def run_shell(command: str) -> str:
    """Execute shell commands."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Command output:\n{result.stdout}"
        else:
            return f"Error during shell command execution: {result.stderr}"
    except Exception as e:
        return f"Error during shell command execution: {str(e)}"
    
tools = [write_file, read_file, run_shell]

models = [
    ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY")),
    ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY_1")),
    ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY_2")),
    ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
]
llm = models[0].with_fallbacks(models[1:])

class AutonomousAgentState(TypedDict):
    task: str
    plan: str
    code: str
    file: str
    execution_output: str
    iteration: int
    evaluation: str
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools):
        self.model = model.bind_tools(tools)
        workflow = StateGraph(AutonomousAgentState)
        workflow.add_node("planner", self.planner)
        workflow.add_node("coder", self.coder)
        workflow.add_node("executor", self.executor)
        workflow.add_node("fixer", self.fixer)
        workflow.add_node("evaluator", self.evaluator)
        workflow.add_conditional_edges(
            "evaluator",
            self.controller,
            {"fixer": "fixer", END: END},
        )
        workflow.add_edge("planner", "coder")
        workflow.add_edge("coder", "executor")   
        workflow.add_edge("fixer", "executor")
        workflow.add_edge("executor", "evaluator")
        workflow.set_entry_point("planner")
        self.workflow = workflow.compile()
    
    def _extract_content(self, response):
        """Extract text content from response, handling both string and list formats."""
        content = response.content
        if isinstance(content, list):
            # Filter out tool calls and extract text
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                elif hasattr(item, 'text'):
                    text_parts.append(item.text)
                elif isinstance(item, str):
                    text_parts.append(item)
            return ''.join(text_parts)
        return str(content) if content else ""

    def planner(self, state: AutonomousAgentState) -> AutonomousAgentState:
        task = state["task"]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert project planner."),
                ("user", "Create a detailed plan to accomplish the following task:\n{task}")
            ]
        )
        response = self.model.invoke(prompt.format_messages(task=task))
        return {**state, "plan": self._extract_content(response), "messages": state["messages"]+[response]}
    
    def coder(self, state: AutonomousAgentState) -> AutonomousAgentState:
        plan = state["plan"]
        prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a software developer. "
         "Choose an appropriate filename and write the full code without markdown."),
        ("user", 
         "Plan:\n{plan}\n\n"
         "Respond in the following format ONLY:\n"
         "FILENAME: <filename>\n"
         "CODE:\n<code>")
    ])        
        response = self.model.invoke(prompt.format_messages(plan=plan))
        content = self._extract_content(response)
        parts = content.split("CODE:")
        if len(parts) < 2:
            raise ValueError(f"Response does not contain 'CODE:' marker. Response: {content}")
        filename_part = parts[0]
        file_path = filename_part.split("FILENAME:")[1].strip().split("\n")[0].strip() if "FILENAME:" in filename_part else "script.py"
        code = parts[1].strip()
        print(code)
        return {**state, "code": code, "file": file_path, "messages": state["messages"]+[response]}
    
    def executor(self, state: AutonomousAgentState) -> AutonomousAgentState:
        write_file.invoke({'file_path': state['file'], 'content': state['code'].replace("```python", "").replace("```", "").strip()})
        output = run_shell.invoke({'command': 'python ' + state['file']})
        return {**state, "execution_output": output, "iteration": state["iteration"] + 1, "messages": state["messages"] + [SystemMessage(content=output)]}
    
    def fixer(self, state: AutonomousAgentState) -> AutonomousAgentState:
        execution_output = state['execution_output']
        if state["evaluation"] == "SUCCESS":
            return state
        prompt = ChatPromptTemplate.from_messages(
            [("system", "You are a skilled software developer."),
             ("user", "Based on the following execution output, identify and fix any issues in the code:\n{execution_output}\n\nIf the execution output shows NO error, return EXACTLY the same code without changes. If there is an error, return the corrected full code that satisfies the task `{task}` only but don't change the filename.")]
        )
        response = self.model.invoke(prompt.format_messages(execution_output=execution_output, task=state['task']))
        content = self._extract_content(response)
        return {**state, "code": content, "messages": state["messages"] + [response]}
    
    def evaluator(self, state: AutonomousAgentState) -> AutonomousAgentState:
        execution_output = state['execution_output']
        task = state['task']
        prompt = ChatPromptTemplate.from_messages(
            [("system", "You are an expert evaluator."),
             ("user", "Evaluate if the following execution output meets the task requirements:\nTask: {task}\nExecution Output: {execution_output}\n\nRespond with ONLY one word: SUCCESS or FAILURE.")]
        )
        response = self.model.invoke(prompt.format_messages(task=task, execution_output=execution_output))
        return {**state, "evaluation": self._extract_content(response).strip().upper(), "messages": state["messages"] + [response]}
    
    def controller(self, state: AutonomousAgentState):
        if state["evaluation"] == "SUCCESS":
            return END
        if state["iteration"] >= 5:
            return END
        return "fixer"

agent = Agent(llm, tools)
initial_state: AutonomousAgentState = {
    "task": "Create a Python script that fetches the IP address of the machine and saves it to a file named 'ip_address.txt'.",
    "plan": "",
    "code": "",
    "file": "",
    "execution_output": "",
    "evaluation": "",
    "iteration": 0,
    "messages": []
}
result = agent.workflow.invoke(initial_state)
print("Final Execution Output:")
print(result['execution_output'])
print("Generated Code:")
print(result['code'])
print("File Path:")
print(result['file'])
print(f"Code saved in file: {result['file']}")