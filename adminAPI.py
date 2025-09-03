from flask import Flask, render_template, request, jsonify
import sqlite3
from connectDb import *
import openai
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import pyodbc
oaiClient = OpenAI(
  #api_key=os.environ['OPENAI_API_KEY']
  api_key="sk-proj-xxxxx"
)
model = "gpt-4o"
assistant_name = "Session Grid Assistant"
assistant_id = None
# assistant_type = 13
tenant_id = 8
doc_store_id = 1
instructions = """
You are a support developer in the insurance industry, who is skilled at analyzing log and activity data to establish the root cause of issues or avenues
of investigation to pursue.
With each prompt, you will be given a set of data to analyze. If there isn't enough for meaningful insights, offer what you can but note that more data would be
a stronger correlation.
"""

system_prompt = """User Sessions Count 
-	Agent Name: contains agent names
-	Session Duration: Total duration of each session for each agent
-	Quote Numbers: The quotation numbers associated with each agent
-	Percentile: Can have the value as 90, 50, 10, or 100
-	Date Range: Selected date range
Sample Output:
-	No. of users in the selected date range (last 24 hours) and percentile (90): 
o	Mitch: 1881 secs
o	Ronny: 1751 secs
o	Jacob: 1746 secs
o	Wilson: 1732 secs
-	Users with multiple sessions in the selected date range:
o	Ronny: 2 sessions
	04/01/2025: 1275 secs
	04/01/2025: 476 secs
-	Users who encountered the same error in multiple sessions:
o	Ronny: Processing Error
-	No. of error occurrences grouped by error type:
o	Security Error: 1
o	Retrieval Error: 1
o	Processing Error: 2 
o	Time Out Error: 1
-	No. of submissions from each agent:
o	Mitch: 1
o	Ronny: 2
o	Jacob: 1
o	Wilson: 1
-	No. of submissions without errors: X
Summarize the data
-	Show the ranking of agents by total session duration from longest to shortest in the selected date range and percentile. If an agent has multiple sessions, display their total session time.
-	Show the number of sessions for each agent along with the date
-	Show the list of errored submissions, grouped by agent and error type
-	Show the agents who encountered the same error multiple times across different sessions
-	Show the number of submissions per agent and the number of successful vs errored submissions
-	Show the error(s) occurrences per agent. If there is any trend for clustering the errored submissions, that should be noted as well
"""

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    conn =  devDbConnection() ##localDbConnection()
    conn.cursor()
    # create_table_sql = '''
    #     IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'assistants' AND xtype = 'U')
    #     BEGIN
    #         CREATE TABLE AssistantType2(
    #            AssistantTypeId int IDENTITY(1,1) NOT NULL,
	#             TypeValue varchar(50) NOT NULL,
    #             Descr nvarchar(1000) NULL,
	#         IsSingleInstance bit NOT NULL,
    #         )
    #     END
    #     '''
    # c.execute(create_table_sql)
    # conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('adminIndex.html')

@app.route('/create_or_update_assistant', methods=['POST'])
def create_or_update():
    ## Fetch form data
    data = request.form
    idOpt = data.get('id')
    asstType = data.get('type')
    asstDescription = data.get('description')
    action = data.get('action')
    is_single_instance_raw = data.get('is_single_instance')  # 'Yes' or 'No'
    is_single_instance = 1 if is_single_instance_raw == 'Yes' else 0
    ## Establish database connection
    conn = localDbConnection()
    c = conn.cursor()

    ## Perform selected action: create, update, delete, or list the assistant
    if action == 'create':
        formTypeValue = idOpt
        formDescr = asstDescription
        # singleInstance = 1
        if asstType == "" and formDescr =="":
            message = message = f"<strong>Please enter the assistant type and description </strong>"
        else:
            # c.execute('SELECT TypeValue1 from AssistantType2 where TypeValue1 =?', (asstType))
            c.execute('SELECT Name from Assistant where AssistantId =?', (idOpt))
            idPresent = c.fetchall()
            if idPresent:
                message = f"<strong>Assistant with {idOpt} is already present </strong> {idPresent}"
                # message = f"<strong>Assistant with {asstType} is already present </strong> {idPresent}"
            else:
                asst = create_assistant(oaiClient, instructions)
                c.execute('INSERT INTO AssistantType2 (TypeValue1, Descr1, IsSingleInstance1) VALUES (?, ?, ?)', (asstType, formDescr, is_single_instance))
                # c.execute('INSERT INTO Assistant1 (ExternalId, Name, WikiDocStoreId, tenantId, SystemPromptText, Instructions, AssistantTypeId) VALUES (?, ?,?, ?, ?,?,?)', (asst.id, assistant_name, doc_store_id, tenant_id, system_prompt, instructions, idOpt ))
                message = f"<strong>Assistant created successfully </strong>(Type: {asstType}, Desc: {asstDescription} and its id is {asst.id})"
                message += f"Assistant details: {asst.id}, <br> {doc_store_id}, <br> {system_prompt}, <br>{instructions},<br>{asstType}"
    elif action == 'update' and idOpt:
        if  asstType == "" and asstDescription =="":
            message = message = f"<strong>Please enter the assistant type and description with new details</strong>"
        else:
            c.execute('SELECT * from AssistantType2 where AssistantTypeId1 =?', (idOpt))
            idPresent = c.fetchall()
            if idPresent:
                c.execute('UPDATE AssistantType2 SET TypeValue1 = ?, Descr1 = ?, IsSingleInstance1 = ? WHERE AssistantTypeId1 = ?', (asstType, asstDescription, is_single_instance, idOpt))
                message = f"<strong>Assistant updated successfully </strong>(ID: {idOpt}, Type: {asstType}, Desc: {asstDescription})"
            else:
                message = f"<strong>Could not find the assistant to update</strong>"
    elif action == 'delete' and idOpt:
        c.execute('SELECT AssistantTypeId1 from AssistantType2 where AssistantTypeId1 =?', (idOpt))
        idPresent = c.fetchall()
        if idPresent:
            c.execute('DELETE FROM AssistantType2 WHERE AssistantTypeId1  = ?', (idOpt,))
            message = f"<strong>Assistant deleted successfully </strong> (ID: {idOpt})"
        else:
            message = f"<strong>Could not find the assistant to delete </strong>"
    elif action== 'list':
        c.execute('SELECT Name from Assistant')
        # c.execute('SELECT TypeValue1 from AssistantType2')
        assts = c.fetchall()
        asstsList = [row[0].strip() for row in assts]
        message = f"<strong>List of assistants: </strong>{' , '.join(asstsList)}"
    elif action == 'asstDetails':
        # c.execute('SELECT AssistantTypeId1 from AssistantType2 where AssistantTypeId1 =?', (idOpt))
        c.execute('SELECT Name, AssistantId from Assistant where AssistantId =?', (idOpt))
        idPresent = c.fetchall()
        if idPresent:
            # c.execute('SELECT * from AssistantType2 where AssistantTypeId1 = ?', (idOpt,))
            c.execute('SELECT * from Assistant where AssistantId = ?', (idOpt,))
            assts = c.fetchall()
            asstsList = [str(row) for row in assts]
            message = f"<strong>List of assistants: </strong>{' , '.join(asstsList)}"
        else:
            message = f"<strong>Could not find the request assistant's details  </strong>"
    else:
        message = f"<strong>No valid action provided or missing ID.</strong>"

    ## Commit the database operation
    conn.commit()

    ## Close the database operation
    conn.close()

    ## Return the results
    return jsonify({'message': message})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5002)

