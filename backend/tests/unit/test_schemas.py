import pytest
from pydantic import ValidationError

from models.schemas import CreateJobRequest, SourceType


def test_valid_youtube_url():
    req = CreateJobRequest(
        source_type="youtube",
        source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    )
    assert req.source_type == SourceType.youtube


def test_valid_youtube_short_url():
    req = CreateJobRequest(
        source_type="youtube",
        source_url="https://youtu.be/dQw4w9WgXcQ",
    )
    assert req.source_type == SourceType.youtube


def test_invalid_youtube_url_raises():
    with pytest.raises(ValidationError):
        CreateJobRequest(
            source_type="youtube",
            source_url="https://vimeo.com/123456",
        )


def test_valid_gdrive_url():
    req = CreateJobRequest(
        source_type="gdrive",
        source_url="https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    )
    assert req.source_type == SourceType.gdrive


def test_invalid_gdrive_url_raises():
    with pytest.raises(ValidationError):
        CreateJobRequest(
            source_type="gdrive",
            source_url="https://dropbox.com/s/abc123/video.mp4",
        )


def test_empty_url_raises():
    with pytest.raises(ValidationError):
        CreateJobRequest(source_type="youtube", source_url="")
