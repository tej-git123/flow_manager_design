# flow_manager_design
A FastAPI application to design a flow manager system


How to run:
1. cd flow_manager_design
2. uvicorn main:app --reload
3. goto - http://127.0.0.1:8000 - to see the welcome greet message in web browser
4. goto - http://127.0.0.1:8000/docs - for Swagger UI to try out the working of the APIs
5. to run the POST /run_flow use the below json data as the input data and try it out
    a. Click 'POST' Button
    b. Click 'Try it out' Button
    c. Use the below json data - copy below json data and paste it into 'Request body' field
    d. Click Execute Button
    e. Check the 'Response Body'
    f. For more details also check the output at the terminal
    g. Two new files get generated - processed.json and stored-data-base.xml
       where processed.json is an temporary file and
       stored-data-base.xml is the XML database file which contains the actual data
6. other GET apis can be run directly to see the output

JSON Data for POST /run_flow api

{
  "flow": {
    "id": "flow123",
    "name": "Data Processing Flow",
    "start_task": "fetch_data",
    "tasks": [
      {"name": "fetch_data", "description": "Fetch data from API"},
      {"name": "process_data", "description": "Process the data"},
      {"name": "store_data", "description": "Store final data"}
    ],
    "conditions": [
      {
        "name": "condition_task1_result",
        "description": "Evaluate the result of task1. If successful, proceed to task2; otherwise, end the flow.",
        "source_task": "fetch_data",
        "outcome": "success",
        "target_task_success": "process_data",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task2_result",
        "description": "Evaluate the result of task2. If successful, proceed to task3; otherwise, end the flow.",
        "source_task": "process_data",
        "outcome": "success",
        "target_task_success": "store_data",
        "target_task_failure": "end"
      }
    ]
  }
}

