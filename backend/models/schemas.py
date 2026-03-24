import re
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class SourceType(str, Enum):
    youtube = "youtube"
    gdrive = "gdrive"


class JobStatus(str, Enum):
    pending = "pending"
    downloading = "downloading"
    chunking = "chunking"
    transcribing = "transcribing"
    analyzing = "analyzing"
    generating = "generating"
    completed = "completed"
    failed = "failed"


class JobProgress(BaseModel):
    step: str
    current: int = 0
    total: Optional[int] = None
    percent: float = 0.0
    eta_seconds: Optional[int] = None
    message: str = ""


class JobMetadata(BaseModel):
    video_title: Optional[str] = None
    video_duration_seconds: Optional[int] = None
    total_chunks: Optional[int] = None


class Job(BaseModel):
    id: str
    source_type: SourceType
    source_url: str
    status: JobStatus = JobStatus.pending
    progress: JobProgress = JobProgress(step="pending")
    metadata: JobMetadata = JobMetadata()
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class CreateJobRequest(BaseModel):
    source_type: SourceType
    source_url: str

    @field_validator("source_url")
    @classmethod
    def validate_source_url(cls, v: str, info) -> str:
        source_type = info.data.get("source_type")
        if source_type == SourceType.youtube:
            if not re.search(
                r"(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]+", v
            ):
                raise ValueError("URL do YouTube inválida")
        elif source_type == SourceType.gdrive:
            if not re.search(
                r"drive\.google\.com/(file/d/|open\?id=)[a-zA-Z0-9_-]+", v
            ):
                raise ValueError("URL do Google Drive inválida")
        return v
