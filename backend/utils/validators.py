"""Utilities for validating video URLs and metadata."""

import subprocess
import json
import logging
from typing import Tuple, Optional, Dict, Any
from backend.core.config import settings


logger = logging.getLogger(__name__)


def get_video_info(url: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve metadata of a video from a URL using yt-dlp.

    Args:
        url (str): Video URL to fetch metadata from.

    Returns:
        Optional[Dict[str, Any]]: Video metadata dictionary or None if failed.
    """
    logger.info(f"[get_video_info] Trying to fetch metadata for: {url}")
    try:
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--print-json", "-f", "bestaudio", url],
            capture_output=True,
            text=True,
            check=False
        )

        logger.debug(f"[get_video_info] yt-dlp returncode: {result.returncode}")
        logger.debug(f"[get_video_info] yt-dlp stdout: {result.stdout[:500]}")
        logger.debug(f"[get_video_info] yt-dlp stderr: {result.stderr}")

        if result.returncode != 0 or not result.stdout.strip():
            logger.error("[get_video_info] yt-dlp failed to fetch metadata.")
            return None

        info = json.loads(result.stdout)
        logger.info(f"[get_video_info] Successfully parsed metadata keys: {list(info.keys())}")
        return info

    except json.JSONDecodeError as e:
        logger.exception(f"[get_video_info] JSON decode error: {e}")
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
    logger.info(f"[validate_video] Validating video: {url}")
    info = get_video_info(url)

    if not info:
        return False, "Could not fetch metadata. This does not look like a valid video URL."

    duration = info.get("duration", 0)
    filesize = info.get("filesize") or info.get("filesize_approx") or 0
    logger.info(f"[validate_video] duration={duration}, filesize={filesize}")

    if duration > settings.max_duration:
        return False, f"The video is longer than {settings.max_duration/60:.1f} minutes."

    if filesize and filesize > settings.max_size:
        return False, f"The video file is larger than {settings.max_size/(1024*1024):.0f} MB."

    return True, info
