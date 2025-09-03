from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connectDb import localDbConnection
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

oaiClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

instructions = """
You are a support developer in the insurance industry, who is skilled at analyzing log and activity data to establish the root cause of issues or avenues
of investigation to pursue.
With each prompt, you will be given a set of data to analyze. If there isn't enough for meaningful insights, offer what you can but note that more data would be
a stronger correlation.
"""

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("adminIndex.html", {"request": request})

@app.post("/create_or_update_assistant")
async def create_or_update_assistant(
    request: Request,
    asstType: str = Form(alias='AssistantId'),
    asstTypeValue: str = Form(alias='TypeValue'),
    asstDescription: str = Form(alias='SysPrompt'),
    action: str = Form(alias='action'),
    is_single_instance_raw: str = Form(alias='is_single_instance', default='No')
):
    is_single_instance = 1 if is_single_instance_raw == 'Yes' else 0
    message = ""

    conn = localDbConnection()
    cursor = conn.cursor()

    if action == 'create':
        cursor.execute('SELECT TypeValue1 FROM AssistantType2 WHERE TypeValue1 = ?', (asstType,))
        id_present = cursor.fetchall()
        if id_present:
            message = f"<strong>Assistant with {asstType} already exists</strong>: {id_present}"
        else:
            asst = oaiClient.beta.assistants.create(
                name="Session Grid Assistant",
                instructions=instructions,
                tools=[{"type": "code_interpreter"}],
                model="gpt-4o"
            )
            cursor.execute(
                'INSERT INTO AssistantType2 (TypeValue1, Descr1, IsSingleInstance1) VALUES (?, ?, ?)',
                (asstType, asstDescription, is_single_instance)
            )
            message = (
                f"<strong>Assistant created successfully</strong> (Type: {asstType}, Desc: {asstDescription}, ID: {asst.id})"
            )

    elif action == 'update':
        cursor.execute('SELECT AssistantTypeId1 FROM AssistantType2 WHERE AssistantTypeId1 = ?', (asstType,))
        if cursor.fetchall():
            cursor.execute(
                'UPDATE AssistantType2 SET TypeValue1 = ?, Descr1 = ?,  IsSingleInstance1=? WHERE AssistantTypeId1 = ?',
                (asstTypeValue, asstDescription, is_single_instance, asstType )
            )
            cursor.commit()
            message = f"<strong>Assistant updated successfully</strong> (ID: {asstType})"
        else:
            message = "<strong>Could not find assistant to update</strong>"

    elif action == 'delete':
        cursor.execute('SELECT AssistantTypeId1 FROM AssistantType2 WHERE AssistantTypeId1 = ?', (asstType,))
        if cursor.fetchall():
            cursor.execute('DELETE FROM AssistantType2 WHERE AssistantTypeId1 = ?', (asstType,))
            message = f"<strong>Assistant deleted successfully</strong> (ID: {asstType})"
        else:
            message = "<strong>Could not find assistant to delete</strong>"

    elif action == 'list':
        cursor.execute('SELECT TypeValue1 FROM AssistantType2')
        items = cursor.fetchall()
        message = "<strong>List of assistants:</strong> " + ", ".join(i[0].strip() for i in items)

    elif action == 'asstDetails':
        cursor.execute('SELECT * FROM AssistantType2 WHERE AssistantTypeId1 = ?', (asstType,))
        row = cursor.fetchall()
        if row:
            message = "<strong>Assistant Details:</strong> " + str(row)
        else:
            message = "<strong>Could not find assistant details</strong>"

    else:
        message = "<strong>Invalid action or missing parameters</strong>"

    conn.commit()
    conn.close()

    return JSONResponse(content={"message": message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("adminAPIFast:app", host="127.0.0.1", port=8000, reload=True)
