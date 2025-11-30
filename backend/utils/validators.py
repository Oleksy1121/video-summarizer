"""Utilities for validating video URLs and metadata."""

import subprocess
import json
import logging
import os
from typing import Tuple, Optional, Dict, Any
from backend.core.config import settings
from backend.utils.secret_manager import get_secret_file_path


logger = logging.getLogger(__name__)

# Pobierz cookies path przy starcie
try:
    cookies_path = get_secret_file_path(project_id="ml-portfolio-xyz123", secret_id="YT_COOCKIES")
    if cookies_path and os.path.exists(cookies_path):
        logger.info(f"[INIT] Cookies file loaded successfully ({os.path.getsize(cookies_path)} bytes)")
    else:
        logger.error(f"[INIT] Cookies file not found at: {cookies_path}")
except Exception as e:
    logger.exception(f"[INIT] Failed to load cookies: {e}")
    cookies_path = None


def get_video_info(url: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve metadata of a video from a URL using yt-dlp.

    Args:
        url (str): Video URL to fetch metadata from.

    Returns:
        Optional[Dict[str, Any]]: Video metadata dictionary or None if failed.
    """
    logger.info(f"[get_video_info] Fetching metadata for: {url}")
    
    if not cookies_path or not os.path.exists(cookies_path):
        logger.error("[get_video_info] Cookies file unavailable")
        return None
    
    try:
        result = subprocess.run(
            ["yt-dlp", "--cookies", cookies_path, "--skip-download", "--print-json", url],
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if result.returncode != 0:
            logger.error(f"[get_video_info] yt-dlp failed (code {result.returncode}): {result.stderr}")
            return None
            
        if not result.stdout.strip():
            logger.error("[get_video_info] Empty response from yt-dlp")
            return None

        info = json.loads(result.stdout)
        logger.info(f"[get_video_info] Successfully fetched metadata")
        return info

    except subprocess.TimeoutExpired:
        logger.error("[get_video_info] Request timed out")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"[get_video_info] JSON parse error: {e}")
        return None
    except Exception as e:
        logger.exception(f"[get_video_info] Unexpected error: {e}")
        return None


def validate_video(url: str) -> Tuple[bool, str]:
    """
    Validate a video URL by checking duration and file size limits.

    Args:
        url (str): Video URL to validate.

    Returns:
        Tuple[bool, str]: (is_valid, message_or_info)
            - If valid: (True, video_info_dict)
            - If invalid: (False, error_message)
    """
    logger.info(f"[validate_video] Validating: {url}")
    info = get_video_info(url)

    if not info:
        return False, "Could not fetch metadata. This does not look like a valid video URL."

    duration = info.get("duration", 0)
    filesize = info.get("filesize") or info.get("filesize_approx") or 0

    if duration > settings.max_duration:
        return False, f"The video is longer than {settings.max_duration/60:.1f} minutes."

    if filesize and filesize > settings.max_size:
        return False, f"The video file is larger than {settings.max_size/(1024*1024):.0f} MB."

    logger.info(f"[validate_video] Validation successful")
    return True, info