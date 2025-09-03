from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import re
import shutil
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_question(question: str) -> str:
    question = re.sub(r'•+', ' ', question)
    question = re.sub(r'\s+', ' ', question).strip()
    question = question.replace("What when", "When")
    question = question.replace("What •", "")
    question = question.replace(": scalable:", "Why is it scalable?")
    if not question.endswith("?") and not question.lower().startswith("explain"):
        question += "?"
    return question

def clean_context(context: str) -> str:
    context = re.sub(r'•+', '', context)
    context = re.sub(r'\s+', ' ', context).strip()
    context = re.sub(r'https?://\S+', '', context)
    context = re.sub(r'For More Such Content.*', '', context, flags=re.IGNORECASE)
    context = re.sub(r'\b\S+@\S+\b', '', context)
    return context

def clean_data(data: List[dict]) -> List[dict]:
    cleaned = []
    for entry in data:
        cleaned_entry = {
            "question": clean_question(entry.get("question", "")),
            "context": clean_context(entry.get("context", "")),
            "source": entry.get("source", "")
        }
        cleaned.append(cleaned_entry)
    return cleaned

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_location = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with open(file_location, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        # Read the lines to show context of the error
        with open(file_location, "r", encoding="utf-8") as f:
            lines = f.readlines()
        error_line = lines[e.lineno - 1].strip() if e.lineno and e.lineno <= len(lines) else "Line not found"
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid JSON file.",
                "detail": str(e),
                "line": e.lineno,
                "line_content": error_line,
                "hint": "Check for missing values, trailing commas, or malformed entries near this line."
            }
        )

    cleaned = clean_data(data)
    output_filename = f"cleaned_{file_id}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4)

    return JSONResponse({
        "message": "File cleaned successfully.",
        "download_url": f"/download/{file_id}",
        "filename": output_filename
    })

@app.get("/download/{file_id}")
def download_file(file_id: str):
    print(f"Searching for file ID: {file_id}")
    for fname in os.listdir(OUTPUT_DIR):
        print(f"Checking file: {fname}")
        if fname == f"cleaned_{file_id}.json":
            return FileResponse(
                path=os.path.join(OUTPUT_DIR, fname),
                filename=fname,
                media_type='application/json'
            )
    return JSONResponse({"error": "File not found"}, status_code=404)

@app.get("/")
def home():
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>LLM Data Cleaner</title>
        </head>
        <body>
            <h1>Upload Your JSON File</h1>
            <form id="upload-form" enctype="multipart/form-data">
                <input type="file" id="file" name="file" accept=".json">
                <br> <br>
                <button type="submit" style="margin:0 auto; width:5%; height: 20px; background-color: #FFB6C1;">Upload & Clean</button>
            </form>
            <div id="result"></div>
            <script>
                document.getElementById("upload-form").addEventListener("submit", async function(e) {
                    e.preventDefault();
                    const fileInput = document.getElementById("file");
                    const formData = new FormData();
                    formData.append("file", fileInput.files[0]);
                    const response = await fetch("/upload/", {
                        method: "POST",
                        body: formData
                    });
                    const result = await response.json();
                    if (response.ok) {
                        document.getElementById("result").innerHTML = `<br/><br/> <a href="${result.download_url}">Download Cleaned JSON</a>`;
                    } else {
                        document.getElementById("result").innerHTML = `
                            <p style='color:red;'><b>${result.error}</b>: ${result.detail}</p>
                            <p><b>Line:</b> ${result.line}</p>
                            <p><b>Content:</b> ${result.line_content}</p>
                            <p><b>Hint:</b> ${result.hint}</p>
                        `;
                    }
                });
            </script>
        </body>
        </html>
    """)
