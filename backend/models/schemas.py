"""Pydantic models for API request/response validation."""

from pydantic import BaseModel, HttpUrl


class VideoURLRequest(BaseModel):
    """Request model for video summarization."""

    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=example"
            }
        }


class SummarizeResponse(BaseModel):
    """Response model for video summarization."""

    summary: str

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "# Video Summary\n\n- Point 1\n- Point 2"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""

    detail: str
