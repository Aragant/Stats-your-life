import os
from dotenv import load_dotenv

# Charger le fichier .env au démarrage
load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET: str = os.getenv("SECRET", "")


settings = Settings()
