import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RULES_FILEPATH: str = os.path.join(BASE_DIR, "app", "data", "rules.json")
    SPECIES_FILEPATH: str = os.path.join(BASE_DIR, "app", "data", "species.json")

    # Credenciales del usuario único experto guardadas directamente en el código
    EXPERT_USERNAME: str = "admin"
    EXPERT_PASSWORD: str = "Admin"

    # Configuración JWT
    JWT_SECRET_KEY: str = "se_crustaceos_grupo4_super_secret_key_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    class Config:
        extra = "ignore"


settings = Settings()
