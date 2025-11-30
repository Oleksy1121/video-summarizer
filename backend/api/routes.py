"""API routes for video summarization."""

import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi.util import get_remote_address
from openai import OpenAI

from backend.models.schemas import VideoURLRequest, SummarizeResponse, ErrorResponse
from backend.api.dependencies import get_openai_client
from backend.services.video_service import summarize_video
from backend.main import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid video URL or validation failed"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Summarize a video from URL",
    description="Downloads audio from a video URL, transcribes it, and generates a summary in Markdown format."
)

@limiter.limit("15 per 4 hours")
def summarize_video_endpoint(
    request: Request,
    video: VideoURLRequest,
    openai_client: OpenAI = Depends(get_openai_client)
) -> SummarizeResponse:
    """
    Summarize a video from a given URL.

    Args:
        video (VideoURLRequest): Request containing the video URL.
        openai_client (OpenAI): Injected OpenAI client dependency.

    Returns:
        SummarizeResponse: Response containing the generated summary.

    Raises:
        HTTPException: If video validation fails or processing error occurs.
    """
    try:
        logger.info(f"Received summarization request for URL: {video.url}")
        summary = summarize_video(url=video.url, openai_client=openai_client)
        return SummarizeResponse(summary=summary)

    except ValueError as e:
        # Validation errors (invalid URL, too long, too large, etc.)
        logger.warning(f"Validation error for URL {video.url}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error processing URL {video.url}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the video. Please try again later."
        )
