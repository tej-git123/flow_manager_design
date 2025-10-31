# # This is a sample Python script.
#
# # Press ⌃R to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from tasks import TASK_DETAILS_DICT, PROCESSED_DATA_FILE

app = FastAPI(title="Generic Flow Manager", version="1.0")

# creating the data models
class Task(BaseModel):
    name: str
    description: str

class Condition(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str

class FlowDefinition(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: List[Task]
    conditions: List[Condition]

class FlowRequest(BaseModel):
    flow: FlowDefinition


def execute_task(task_name: str) -> bool:
    """Execute the added task from task-dict dynamically."""
    task_func = TASK_DETAILS_DICT.get(task_name)
    if not task_func:
        print(f"Task '{task_name}' not found in task-dict.")
        return False

    try:
        result = task_func()
        return bool(result)
    except Exception as e:
        print(f"Error executing task '{task_name}': {e}")
        return False


def run_flow(flow: FlowDefinition) -> Dict:
    """Run a flow sequentially according to its conditions."""
    tasks_map = {task.name: task for task in flow.tasks}
    conditions_map = {cond.source_task: cond for cond in flow.conditions}

    current_task_name = flow.start_task
    executed = []

    print(f"\nStarting flow '{flow.name}' (ID: {flow.id})\n")

    while current_task_name and current_task_name != "end":
        if current_task_name not in tasks_map:
            raise HTTPException(status_code=400, detail=f"Task '{current_task_name}' not defined in flow")

        success = execute_task(current_task_name)
        executed.append({"task": current_task_name, "success": success})

        condition = conditions_map.get(current_task_name)
        if not condition:
            break

        current_task_name = (
            condition.target_task_success if success else condition.target_task_failure
        )

    print("\nFlow completed.\n")
    print("Showing Details")
    print({"flow_id": flow.id, "executed_tasks": executed})
    return {"flow_id": flow.id, "executed_tasks": executed}


# creating API endpoints
@app.get("/")
def root():
    return {"message": "Welcome to the Flow Manager API"}


@app.get("/show_data")
def show_data():
    data = json.loads(PROCESSED_DATA_FILE.read_text())
    return {"data": data}

@app.get("/tasks")
def list_tasks():
    return {"registered_tasks": list(TASK_DETAILS_DICT.keys())}

@app.post("/run_flow")
def run_flow_api(request: FlowRequest):
    result = run_flow(request.flow)
    return {"status": "completed", "result": result}






