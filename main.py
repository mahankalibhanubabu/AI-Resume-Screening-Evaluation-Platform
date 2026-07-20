from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil

# Create FastAPI app
app = FastAPI(
    title="Resume Upload API",
    description="Backend API for uploading resumes",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Backend Running Successfully!"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/upload")
async def upload_resume(
    candidateName: str = Form(...),
    email: str = Form(...),
    jobRole: str = Form(...),
    resume: UploadFile = File(...)
):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    return {
        "status": "success",
        "message": "Resume Uploaded Successfully!",
        "candidateName": candidateName,
        "email": email,
        "jobRole": jobRole,
        "uploadedFile": resume.filename,
        "savedPath": file_path
    }


@app.get("/files")
def list_uploaded_files():
    files = os.listdir(UPLOAD_FOLDER)

    return {
        "totalFiles": len(files),
        "files": files
    }


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {
            "status": "success",
            "message": f"{filename} deleted successfully."
        }

    return {
        "status": "error",
        "message": "File not found."
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )