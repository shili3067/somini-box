import yt_dlp
import os
import threading
import uuid
import time
from typing import Dict, Any
import imageio_ffmpeg
from core.extractor import clean_error_message

# Global memory to track download status
download_tasks: Dict[str, Dict[str, Any]] = {}

def update_progress(d, task_id):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        speed = d.get('speed', 0)
        
        percent = 0
        if total and total > 0:
            percent = (downloaded / total) * 100
            
        download_tasks[task_id].update({
            'status': 'downloading',
            'percent': round(percent, 2),
            'speed': speed,
            'downloaded': downloaded,
            'total': total or 0
        })
    elif d['status'] == 'finished':
        download_tasks[task_id].update({
            'status': 'processing',
            'percent': 100
        })

def download_video_thread(url: str, task_id: str):
    import shutil
    # Store temporarily with task_id to isolate the file
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'OmniVid_Tmp', task_id)
    os.makedirs(download_dir, exist_ok=True)
    
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'progress_hooks': [lambda d: update_progress(d, task_id)],
        'ffmpeg_location': ffmpeg_path,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Locate the fully downloaded and merged file
        files = os.listdir(download_dir)
        final_file = ""
        for f in files:
            # exclude temp files from yt-dlp
            if not f.endswith('.part') and not f.endswith('.ytdl'):
                final_file = os.path.join(download_dir, f)
                break
                
        if final_file:
            download_tasks[task_id]['status'] = 'completed'
            download_tasks[task_id]['file_path'] = final_file
        else:
            raise Exception("File merging failed or file not found")
    except Exception as e:
        download_tasks[task_id]['status'] = 'failed'
        download_tasks[task_id]['error'] = clean_error_message(str(e))

def start_download(url: str) -> str:
    """Start a background download and return tracking ID."""
    task_id = str(uuid.uuid4())
    download_tasks[task_id] = {
        'id': task_id,
        'url': url,
        'status': 'starting',
        'percent': 0,
        'speed': 0,
        'error': None
    }
    
    thread = threading.Thread(target=download_video_thread, args=(url, task_id))
    thread.daemon = True
    thread.start()
    
    return task_id

def get_download_status(task_id: str) -> Dict[str, Any]:
    """Get the current progress of a download."""
    return download_tasks.get(task_id, {'status': 'not_found'})
