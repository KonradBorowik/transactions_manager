import os
from dotenv import load_dotenv

env_mode = os.getenv("ENV", "development")

if env_mode == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

DATABASE_URL = os.getenv("DATABASE_URL")