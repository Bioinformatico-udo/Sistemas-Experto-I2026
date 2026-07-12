import os
from pydantic import BaseModel

class Settings(BaseModel):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RULES_FILEPATH: str = os.path.join(BASE_DIR, "app", "data", "rules.json")
    SPECIES_FILEPATH: str = os.path.join(BASE_DIR, "app", "data", "species.json")

settings = Settings()
