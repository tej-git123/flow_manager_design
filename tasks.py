import os
import json
import time
from pathlib import Path

DATA_FILE = Path("data.json")   # data input file
PROCESSED_DATA_FILE = Path("processed.json")    # file after doing some processing on input file
DATABASE_FILE = Path("stored-data-base.xml")    # file to create the xml database

TASK_DETAILS_DICT = {}  # dictionary for adding all the tasks here

# creating xml database
import xml.etree.ElementTree as et
def build_xml_database():
    """creating a xml database tree and dumping the records to this database"""
    data = json.loads(PROCESSED_DATA_FILE.read_text())
    db = et.Element('database')

    keys = list(data.keys())
    for each in keys:
        db_data = et.SubElement(db, 'employee_records')
        for record in data[each]:
            emp_record = et.SubElement(db_data, 'employee')
            emp_id = et.SubElement(emp_record, 'id')
            emp_name = et.SubElement(emp_record, 'name')
            emp_salary = et.SubElement(emp_record, 'salary')
            emp_bonus = et.SubElement(emp_record, 'bonus')

            emp_id.text = str(record['id'])
            emp_name.text = str(record['name'])
            emp_salary.text = str(record['salary'])
            emp_bonus.text = str(record['bonus'])
    et.indent(db, space="    ", level=0)
    xml_tree = et.ElementTree(db)
    xml_tree.write(DATABASE_FILE)


def register_task(name):
    """Decorator to add a task in the global task-dict."""
    def wrapper(func):
        TASK_DETAILS_DICT[name] = func
        return func
    return wrapper


@register_task("fetch_data")
def fetch_data():
    """Fteching the data from the input json file"""
    print("Fetching data...")
    data = json.loads(DATA_FILE.read_text())
    if data:
        print("Data fetched successfully..!!")
        return True
    else:
        print("FAILURE: Data fetching failed..!!")
        return False


@register_task("process_data")
def process_data():
    """loading the input json file and doing some processing on it"""
    print("Processing data...")
    data = json.loads(DATA_FILE.read_text())
    data["employees"] = [u for u in data["employees"] if "name" in u]
    for employee in data["employees"]:
        employee.update({"bonus": employee["salary"] + 10000})
    PROCESSED_DATA_FILE.write_text(json.dumps(data))
    if os.path.exists(PROCESSED_DATA_FILE):
        print("Data processed successfully..!!")
        return True
    else:
        print("FAILUER: Data processing Failed since no processing file dumped..!!")
        return False


@register_task("store_data")
def store_data():
    """Storing the data to the XML database"""
    print("Storing data to the XML database..")
    build_xml_database()
    time.sleep(1)
    if os.path.exists(DATABASE_FILE):
        print("Data stored successfully..!!")
        return True
    else:
        print("FAILURE: Data storing Failed since no DB file dumped..!!")
        return False




