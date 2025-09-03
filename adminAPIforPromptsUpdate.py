from flask import Flask, render_template, request, jsonify
import sqlite3
from connectDb import *
import openai
from datetime import datetime
import os
from openai import OpenAI
from fastapi.responses import JSONResponse, HTMLResponse
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import pyodbc
oaiClient = OpenAI(
  #api_key=os.environ['OPENAI_API_KEY']
  api_key="sk-proj-uQSDdU85medcLVniY9zyT3BlbkFJeCmlqDo8iSgoHkJBcDiP"
)
assistant ={}
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

system_prompt =""

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    conn =  devDbConnection() ##localDbConnection()

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
    return conn

@app.route('/')
def index():
    return render_template('adminIndex.html')

# @app.route('/create_or_update_assistant', methods=['POST'])
# def create_or_update():
#     ## Fetch form data
#     data = request.form
#     idOpt = data.get('id')
#     asstType = data.get('type')
#     asstDescription = data.get('description')
#     action = data.get('action')
#     is_single_instance_raw = data.get('is_single_instance')  # 'Yes' or 'No'
#     is_single_instance = 1 if is_single_instance_raw == 'Yes' else 0
#     ## Establish database connection
#     conn = init_db()
#     c = conn.cursor()
#     current_id = None
#     if action == 'update':
#         if  asstDescription =="" and asstType=="":
#             message = message = f"<strong>Please enter the assistant Id and description with new details</strong>"
#         else:
#             message= f"{action}, {asstType}, {asstDescription}"
#             c.execute('SELECT SystemPromptText from Assistant where AssistantId =?', (int(asstType),))
#             idPresent = c.fetchall()
#             asstsList = [str(row) for row in idPresent]
#             message = f"<strong>List of assistants: </strong> {asstsList}"  #{' , '.join(asstsList)}"
#             if idPresent:
#                 c.execute('UPDATE Assistant SET SystemPromptText = ? WHERE AssistantId = ?', (asstDescription, (int(asstType),)))
#                 conn.commit()
#                 message = f"<strong>Assistant updated successfully </strong>(ID: {asstType},  Desc: {asstDescription})"
#             else:
#                 message = f"<strong>Could not find the assistant to update</strong>"
#     elif action == 'list':
#         c.execute('SELECT Name, AssistantId from Assistant where AssistantId  > ?', (31,))
#         # c.execute('SELECT TypeValue1 from AssistantType2')
#         assts = c.fetchall()
#         # asstsList = [row[0].strip() for row in assts]
#         # assts1 = assts [0]
#         # # message = f"<strong>List of assistants: </strong><ol> <br/>{'<br/>'.join(asstsList)}"
#         # message = f"<strong>List of assistants: </strong><ol style='text-align: left; margin-left: 30px;'><li>{'</li><li>'.join(asstsList)}<br/></li></ol> "
#         # Format each list item as "AssistantId - Name"
#         # asstsList = [f"{row[1]} - {row[0].strip()}" for row in assts]
#         #
#         # # Create the HTML message
#         # message = f"<strong>List of assistants: </strong><ol style='text-align: left; margin-left: 30px;'>"
#         # message += ''.join([f"<li>{item}</li>" for item in asstsList])
#         # message += "</ol>"
#         message = """
#                <br/><strong>List of Assistants:</strong><br/>
#                <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin-top: 10px; display: inline-table;">
#                    <thead>
#                        <tr>
#                            <th>Assistant ID</th>
#                            <th>Name</th>
#                        </tr>
#                    </thead>
#                    <tbody>
#            """
#         for row in assts:
#             message += f"<tr><td >{row[1]}</td> <td style='text-align: left;'>{row[0].strip()}</td></tr>"
#         message += "</tbody></table>"
#
#     elif action == 'asstDetails':
#         # c.execute('SELECT AssistantTypeId1 from AssistantType2 where AssistantTypeId1 =?', (idOpt))
#         if asstType and asstType.isdigit():
#             asst_id = int(asstType)
#             c.execute('SELECT  AssistantId, Name, SystemPromptText from Assistant where AssistantId =?', asst_id)
#             idPresent = c.fetchall()
#             if idPresent:
#                 # c.execute('SELECT * from AssistantType2 where AssistantTypeId1 = ?', (idOpt,))
#                 c.execute('SELECT AssistantId, Name, SystemPromptText from Assistant where AssistantId = ?',  asst_id)
#                 assts = c.fetchone()
#                 # asstsList = [str(row) for row in assts]
#                 # message = f"<strong>Details of assistant {asstType}: </strong> <br/><strong> System Prompt : </strong> {' , '.join(asstsList)}"
#                 # asst = assts[0]
#                 # message = f"""
#                 # <strong>Details of assistant {asstType}:</strong><br/>
#                 # <strong>Name:</strong> {asst[1]}<br/>
#                 # <strong>System Prompt:</strong>{asst[2]}
#                 # """
#                 # current_id = asstType
#
#                 message = f"""
#                             <br/><strong>Details of Assistant:</strong><br/>
#
#                             <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin-top: 10px; margin-left: auto; margin-right: auto;">
#                                 <thead>
#                                     <tr>
#                                         <th>Assistant ID</th>
#                                         <th>Name</th>
#                                         <th>System Prompt</th>
#                                     </tr>
#                                 </thead>
#                                 <tbody>
#                                     <tr>
#                                         <td>{assts[0]}</td>
#                                         <td style="text-align: left;">{assts[1]}</td>
#                                         <td style="text-align: left;">{assts[2]}</td>
#
#                                     </tr>
#                                 </tbody>
#                             </table>
#                         """
#         else:
#             message = f"<strong>Could not find the request assistant's details  </strong>"
#     # else:
#     #     message = f"<strong>No valid action provided or missing ID.</strong>"
#     elif action == 'first':
#         c.execute('SELECT AssistantId, Name, SystemPromptText from Assistant where AssistantId  > ?', (31,))
#         assts = c.fetchone()
#         current_id = assts[0]
#         message = f"""
#                     <strong>Details of assistant :</strong><br/>
#                     <strong>AssistantId:</strong> {assts[0]}<br/>
#                     <strong>Name:</strong>{assts[1]}<br/>
#                     <strong>System Prompt:</strong>{assts[2]}
#                     """
#         # current_id = assts[0]
#     elif action == 'last':
#         c.execute('SELECT AssistantId, Name, SystemPromptText from Assistant order by AssistantId  desc')
#         assts = c.fetchone()
#         current_id = assts[0]
#         message = f"""
#                     <strong>Details of assistant {asstType}:</strong><br/>
#                     <strong>AssistantId:</strong> {assts[0]}<br/>
#                     <strong>Name:</strong>{assts[1]}<br/>
#                     <strong>System Prompt:</strong>{assts[2]}
#                     """
#         # current_id = assts[0]
#     elif action == 'next':
#         # cur_id = int(request.form.get('AssistantId', 0))
#
#         c.execute('SELECT top 1 AssistantId, Name, SystemPromptText from Assistant where AssistantId  > ? order by AssistantId asc', (current_id, ))
#         assts = c.fetchone()
#         if assts:
#             current_id = assts[0]
#             message = f"""
#                         <strong>Details of assistant {asstType}:</strong><br/>
#                         <strong>AssistantId:</strong> {assts[0]}<br/>
#                         <strong>Name:</strong>{assts[1]}<br/>
#                         <strong>System Prompt:</strong>{assts[2]}
#                         """
#             # current_id = asstType
#         else:
#             message = "No next assistant found"
#     elif action == 'previous':
#         # current_id = int(request.form.get('current_id', 0))
#         c.execute('''
#             SELECT Name, AssistantId, SystemPrompt
#             FROM Assistant
#             WHERE AssistantId < ?
#             ORDER BY AssistantId DESC
#             LIMIT 1
#         ''', (current_id,))
#         assts = c.fetchone()
#         if assts:
#             current_id = assts[0]
#             message = f"""
#                 <strong>Details of assistant {asstType}:</strong><br/>
#                 <strong>Name:</strong> {assts[0]}<br/>
#                 <strong>System Prompt:</strong> {assts[2]}
#             """
#             current_id = asstType
#         else:
#             message = "No previous assistant found."
#     else:
#         message = f"<strong>No valid action provided or missing ID.</strong>"
#     ## Commit the database operation
#         conn.commit()
#
#         ## Close the database operation
#         conn.close()
#
#     ## Return the results
#     return  jsonify({'message': message})

@app.route('/create_or_update_assistant', methods=['POST', 'GET'])
def create_or_update():
    data = request.form
    asstType = data.get('AssistantId')
    TypeVal = data.get('TypeValue')
    asstDescription = data.get('SysPrompt')
    action = data.get('action')
    is_single_instance_raw = data.get('is_single_instance')
    is_single_instance = 1 if is_single_instance_raw == 'Yes' else 0

    conn = init_db()
    c = conn.cursor()
    current_id = None

    if action == 'update':
        if not asstType or not asstDescription:
            message = "<strong>Please enter both the assistant ID and new description.</strong>"
        elif not asstType.isdigit():
            message = "<strong>Assistant ID must be numeric.</strong>"
        else:
            asst_id = int(asstType)
            c.execute('SELECT SystemPromptText FROM Assistant WHERE AssistantId = ?', (asst_id,))
            idPresent = c.fetchall()
            if idPresent:
                c.execute('UPDATE Assistant SET SystemPromptText = ? WHERE AssistantId = ?', (asstDescription, asst_id))
                conn.commit()
                message = f"<strong>Assistant updated successfully</strong> (ID: {asst_id}, Desc: {asstDescription})"
            else:
                message = "<strong>Could not find the assistant to update.</strong>"

    elif action == 'list':
        c.execute('SELECT Name, AssistantId FROM Assistant WHERE AssistantId > ?', (31,))
        assts = c.fetchall()
        message = """
            <br/><strong>List of Assistants:</strong><br/>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin-top: 10px; display: inline-table;">
                <thead>
                    <tr>
                        <th>Assistant ID</th>
                        <th>Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        """
        for row in assts:
            message += f"""
                <tr>
                    <td>{row[1]}</td>
                    <td style='text-align: left;'>{row[0].strip()}</td>
                    <td>
                        <button onclick="editAssistant({row[1]})">Edit</button>
                        <button onclick="deleteAssistant({row[1]})">Delete</button>
                    </td>
                </tr>
            """
        message += "</tbody></table>"

    elif action == 'asstDetails':
        if asstType and asstType.isdigit():
            asst_id = int(asstType)
            c.execute('SELECT AssistantId, Name, SystemPromptText FROM Assistant WHERE AssistantId = ?', (asst_id,))
            idPresent = c.fetchone()
            if idPresent:
                c.execute('SELECT AssistantId, Name, SystemPromptText FROM Assistant WHERE AssistantId = ?', (asst_id,))
                assts = c.fetchone()

                # if assts:
                #     assistant_id, name, system_prompt = assts
                #     return render_template('adminIndex.html',
                #                            AssistantId=assts[0],
                #                            TypeValue=assts[1],
                #                            SysPrompt=assts[2])
                # else:
                #     return render_template('adminIndex.html', message="Assistant not found!")
                message = f"""
                    <br/><strong>Details of Assistant:</strong><br/>
                    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin-top: 10px; margin-left: auto; margin-right: auto;">
                        <thead>
                            <tr>
                                <th>Assistant ID</th>
                                <th>Name</th>
                                <th>System Prompt</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{assts[0]}</td>
                                <td style="text-align: left;">{assts[1]}</td>
                                <td style="text-align: left;">{assts[2]}</td>
                            </tr>
                        </tbody>
                    </table>
                """
            else:
                message = "<strong>Could not find the requested assistant's details.</strong>"
            # return render_template('adminIndex.html', message=message, AssistantId = asst_id, TypeValue = typeVal, SysPrompt=sysPrompt)
        else:
            message = "<strong>Invalid or missing Assistant ID.</strong>"

    elif action == 'first':
        c.execute('SELECT AssistantId, Name, SystemPromptText FROM Assistant WHERE AssistantId > ?', (31,))
        assts = c.fetchone()
        if assts:
            current_id = assts[0]
            message = f"""
                <strong>Details of assistant:</strong><br/>
                <strong>AssistantId:</strong> {assts[0]}<br/>
                <strong>Name:</strong> {assts[1]}<br/>
                <strong>System Prompt:</strong> {assts[2]}
            """
        else:
            message = "<strong>No assistants found.</strong>"

    elif action == 'last':
        c.execute('SELECT AssistantId, Name, SystemPromptText FROM Assistant ORDER BY AssistantId DESC')
        assts = c.fetchone()
        if assts:
            current_id = assts[0]
            message = f"""
                <strong>Details of assistant:</strong><br/>
                <strong>AssistantId:</strong> {assts[0]}<br/>
                <strong>Name:</strong> {assts[1]}<br/>
                <strong>System Prompt:</strong> {assts[2]}
            """
        else:
            message = "<strong>No assistants found.</strong>"

    elif action == 'next':
        if asstType and asstType.isdigit():
            asst_id = int(asstType)
            c.execute('SELECT TOP 1 AssistantId, Name, SystemPromptText FROM Assistant WHERE AssistantId > ? ORDER BY AssistantId ASC', (asst_id,))
            assts = c.fetchone()
            if assts:
                current_id = assts[0]
                message = f"""
                    <strong>Details of assistant:</strong><br/>
                    <strong>AssistantId:</strong> {assts[0]}<br/>
                    <strong>Name:</strong> {assts[1]}<br/>
                    <strong>System Prompt:</strong> {assts[2]}
                """
            else:
                message = "<strong>No next assistant found.</strong>"
        else:
            message = "<strong>Invalid or missing Assistant ID for next.</strong>"
    elif action == 'previous':
        if asstType and asstType.isdigit():
            asst_id = int(asstType)
            c.execute('SELECT TOP 1 AssistantId, Name, SystemPromptText FROM Assistant WHERE AssistantId < ? ORDER BY AssistantId DESC', (asst_id,))
            assts = c.fetchone()
            if assts:
                current_id = assts[0]
                message = f"""
                    <strong>Details of assistant:</strong><br/>
                    <strong>AssistantId:</strong> {assts[0]}<br/>
                    <strong>Name:</strong> {assts[1]}<br/>
                    <strong>System Prompt:</strong> {assts[2]}
                """
            else:
                message = "<strong>No previous assistant found.</strong>"
        else:
            message = "<strong>Invalid or missing Assistant ID for previous.</strong>"
    else:
        message = "<strong>No valid action provided.</strong>"

    conn.commit()
    conn.close()
    return jsonify({'message': message})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5002)
