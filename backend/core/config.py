from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Engine selection
    engine: str = "ollama"
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3.2"

    # Anthropic
    anthropic_api_key: str
    model: str 

    app_port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings() 
