import pyodbc
from datetime import datetime
## Function to connect to local db
def localDbConnection():
    server = 'LAPTOP-LGD807PJ\\SQLEXPRESS'  # e.g., 'localhost' or 'myserver.database.windows.net'
    database = 'Staging_Web_Interactions_18Mar25_Bkp'
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(connection_string)
    return conn

## Function to connect to server db
def devDbConnection():
    server = 'tp-dev-sql.database.windows.net'  # e.g., 'localhost' or 'myserver.database.windows.net'
    database = 'Staging_Web_Interactions'
    username = 'sqladmin'
    password = 'TPDon#2024'
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    conn = pyodbc.connect(connection_string)
    return conn
    # return connection_string

## Function to create a new assistant
def create_assistant(client, instructions):
    asst = client.beta.assistants.create(
        name="Assistant 1",
        instructions=instructions,
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}]
        # tool_resources={
        #   "code_interpreter": {
        #     "file_ids": [file.id]
        #   }
        # }
    )
    print(" Assistant created successfully!")
    return asst

## Function to update an existing assistant
def update_assistant(client, asst_id, new_instructions):
    """
    Updates an assistant in the specified project.
    Args:
        client (AssistantClient): The client to use for making API calls.
        asst_id (str): The ID of the assistant to """
    my_updated_assistant = client.beta.assistants.update(
    assistant_id = asst_id,
    instructions=new_instructions,
    name="Financial Lead",
    tools=[{"type": "file_search"}],
    model="gpt-4o"
  )
    print ("Assistant updated successfully!")
    return my_updated_assistant

## Function to delete all assistants created before a specific date

##  ------------------ Work in progress ------------------
# def delete_old_assistants(del_before_date, saved_list):
#     # Convert delete_before_date to a Unix timestamp
#     delete_before_timestamp = int(datetime.strptime(del_before_date, "%Y-%m-%d").timestamp())
#     conn = localDbConnection()
#     c = conn.cursor()
#
#     c.execute('SELECT * from assistants ')
#     assts = c.fetchall()
#     asstsList = [row[0].strip() for row in assts]