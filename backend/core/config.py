from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    frontend_url: str = "http://localhost:3000"
    outputs_dir: str = "/app/outputs"
    whisper_model: str = "medium"
    whisper_language: str = "pt"
    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.1:8b"
    google_credentials_path: str = "/app/credentials/google-credentials.json"
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
