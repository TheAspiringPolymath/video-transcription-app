from core.config import Settings


def test_default_frontend_url():
    s = Settings()
    assert s.frontend_url == "http://localhost:3000"


def test_default_redis_url():
    s = Settings()
    assert s.redis_url == "redis://redis:6379/0"


def test_default_whisper_model():
    s = Settings()
    assert s.whisper_model == "medium"


def test_openai_api_key_defaults_to_empty_string():
    s = Settings()
    assert s.openai_api_key == ""
    assert s.openai_api_key is not None


def test_default_llm_provider():
    s = Settings()
    assert s.llm_provider == "openai"


def test_default_outputs_dir():
    s = Settings()
    assert s.outputs_dir == "/app/outputs"
