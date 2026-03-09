import yt_dlp
import re
from typing import Dict, Any

def clean_error_message(msg: str) -> str:
    """Remove ANSI escape codes and translate common errors."""
    # Remove ANSI codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_msg = ansi_escape.sub('', msg).strip()
    
    # Check for specific known errors
    if "No video could be found in this tweet" in clean_msg:
        return "在此推文中未找到可用的视频或GIF，或是由于推特接口限制无法抓取。"
    if "Sign in to confirm your age" in clean_msg:
        return "该视频存在年龄限制，需配置 Cookie 登录后抓取。"
    if "Private video" in clean_msg or "private" in clean_msg.lower():
        return "该视频为私有/仅粉丝可见，无法抓取。"
    if "Video unavailable" in clean_msg:
        return "该视频已被下架或在当前地区不可用。"
        
    # Strip the generic 'ERROR: ' prefix for general errors
    if "ERROR:" in clean_msg:
        clean_msg = clean_msg.split("ERROR:", 1)[-1].strip()
        
    return clean_msg

def resolve_video(url: str) -> Dict[str, Any]:
    """
    Resolve video URL to get direct formats and video info.
    """
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'nocheckcertificate': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise Exception("无法提取到该视频的详细信息。")
            
            # Extract essential fields
            return {
                'id': info.get('id', ''),
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': info.get('formats', []),
                'url': url,
                'extractor': info.get('extractor', 'unknown')
            }
        except yt_dlp.utils.DownloadError as e:
            raise Exception(clean_error_message(str(e)))
        except Exception as e:
            raise Exception(f"解析失败: {clean_error_message(str(e))}")

