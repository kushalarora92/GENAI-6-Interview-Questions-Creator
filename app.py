# modular approach

# create a fastapi app

from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status, UploadFile
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

import uvicorn
import os
import aiofiles
import json
import csv
import shutil
from pathlib import Path
import awsgi

from src.helper import llm_pipeline

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Create directories if they don't exist
os.makedirs("static/docs", exist_ok=True)
os.makedirs("static/output", exist_ok=True)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def add_csv(file_path):
    pdf_path = f"static/docs/{file_path}"
    filtered_ques_list, answer_gen_chain = llm_pipeline(pdf_path)

    csv_path = f"static/output/{file_path.replace('.pdf', '.csv')}"
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Answer'])
        for question in filtered_ques_list:
            answer = answer_gen_chain.run(question)
            writer.writerow([question, answer])

    return csv_path

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file to static/docs
        file_path = f"static/docs/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "message": "File uploaded successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyse")
async def analyse_file(request: Request):
    try:
        # Get JSON data from request body
        data = await request.json()
        filename = data.get('filename')
        
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required")
            
        # Get the PDF path
        pdf_path = f"static/docs/{filename}"
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Generate CSV
        csv_path = add_csv(filename)
        
        return JSONResponse({
            "success": True,
            "filepath": csv_path,
            "message": "Analysis completed"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"static/output/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

def handler(event, context):
    return awsgi.response(app, event, context)
