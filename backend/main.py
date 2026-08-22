from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "FManager backend running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": safe_filename
    }

@app.get("/files")
def get_files():
    if not os.path.exists(UPLOAD_DIR):
        return []
        
    files = os.listdir(UPLOAD_DIR)
    result = []

    for filename in files:
        path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(path):
            result.append({
                "name": filename,
                "size": os.path.getsize(path)
            })

    return result
