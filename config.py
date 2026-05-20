from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if os.environ.get("RENDER"):
        SQLALCHEMY_DATABASE_URI = "sqlite:////var/data/users.db"
    else:
        db_path = os.path.join(BASE_DIR, "instance", "users.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False