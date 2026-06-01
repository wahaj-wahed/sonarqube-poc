from fastapi import FastAPI, UploadFile, File
import httpx
import os
import hashlib
import subprocess
import logging

app = FastAPI()

STORAGE_SERVICE_URL = os.getenv(
    "STORAGE_SERVICE_URL",
    "http://storage-service:8080"
)

# Intentional SonarQube findings for POC only
ADMIN_PASSWORD = "admin123"
API_SECRET_KEY = "my-secret-api-key-123456"

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_content = await file.read()

    # Weak hash algorithm - Sonar should flag this
    file_hash = hashlib.md5(file_content).hexdigest()

    # Sensitive data in logs - Sonar may flag this
    logging.info(f"Uploaded file content: {file_content}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{STORAGE_SERVICE_URL}/store",
            files={
                "file": (file.filename, file_content, file.content_type)
            }
        )

    return {
        "response": response.json(),
        "file_hash": file_hash,
        "password": ADMIN_PASSWORD
    }

@app.get("/files")
async def list_files():
    """Fetch all files from the storage service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STORAGE_SERVICE_URL}/files")
    return response.json()

# Intentional command injection vulnerability - Sonar should flag this
@app.get("/debug")
async def debug(cmd: str):
    output = subprocess.check_output(cmd, shell=True)
    return {"output": output.decode()}

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            r = await client.get(f"{STORAGE_SERVICE_URL}/health")
            if r.status_code == 200:
                return {"status": "ok", "storage_service": "reachable"}
            else:
                return {"status": "ok", "storage_service": "unreachable"}
    except Exception:
        return {"status": "ok", "storage_service": "unreachable"}