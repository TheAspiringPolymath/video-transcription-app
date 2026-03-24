class JobNotFoundError(Exception):
    """Raised when a job_id is not found in the filesystem."""


class VideoPrivateError(Exception):
    """Raised when a YouTube video is private or age-restricted."""


class VideoUnavailableError(Exception):
    """Raised when a YouTube video is deleted or otherwise unavailable."""


class DrivePermissionError(Exception):
    """Raised when Google Drive access is denied for the requested file."""


class PipelineError(Exception):
    """Base exception for generic pipeline processing failures."""
