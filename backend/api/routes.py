from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
import shutil
import urllib.parse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.extractor import resolve_video

app = FastAPI(title="OmniVid API")

# Define request schemas
class ResolveRequest(BaseModel):
    url: str
    
class InfoResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "OmniVid Backend is running"}

@app.post("/api/resolve", response_model=InfoResponse)
def resolve_url(request: ResolveRequest):
    try:
        info = resolve_video(request.url)
        return InfoResponse(success=True, data=info)
    except Exception as e:
        return InfoResponse(success=False, error=str(e))
from core.downloader import start_download, get_download_status

class DownloadRequest(BaseModel):
    url: str

class DownloadResponse(BaseModel):
    success: bool
    task_id: Optional[str] = None
    error: Optional[str] = None

@app.post("/api/download", response_model=DownloadResponse)
def trigger_download(request: DownloadRequest):
    try:
        task_id = start_download(request.url)
        return DownloadResponse(success=True, task_id=task_id)
    except Exception as e:
        return DownloadResponse(success=False, error=str(e))

@app.get("/api/download/{task_id}")
def check_download_status(task_id: str):
    return get_download_status(task_id)

@app.get("/api/download/file/{task_id}")
def download_task_file(task_id: str):
    status = get_download_status(task_id)
    if status.get('status') == 'completed' and 'file_path' in status:
        file_path = status['file_path']
        filename = os.path.basename(file_path)
        encoded_filename = urllib.parse.quote(filename)
        folder_path = os.path.dirname(file_path)
        
        return FileResponse(
            path=file_path,
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}"
            },
            # Automatically delete the temp folder after the response is sent to the browser
            background=BackgroundTask(shutil.rmtree, folder_path, ignore_errors=True)
        )
        
    raise HTTPException(status_code=404, detail="File is not ready or has been deleted.")
