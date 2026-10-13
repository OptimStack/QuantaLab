from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str = "dev-secret-change-me"
    database_url: str = "sqlite+aiosqlite:///./quantalab.db"
    redis_url: str = "redis://localhost:6379/0"
    ai_provider: str = "anthropic"
    ai_provider_api_key: str = ""
    ai_provider_model: str = ""
    sandbox_image_name: str = "quantalab-sandbox"
    sandbox_cpu_limit: int = 1
    sandbox_memory_limit_mb: int = 512
    sandbox_timeout_seconds: int = 15
    max_circuit_qubits: int = 16
    cors_allowed_origin: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"

settings = Settings()
