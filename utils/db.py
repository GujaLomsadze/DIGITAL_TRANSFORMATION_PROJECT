from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.load_config import get_config

env_conf, openai_conf, db_conf = get_config()

port = "5432"
host = "db"

if env_conf["env"] == "local":
    port = "5431"
    host = "localhost"

DATABASE_URL = f"postgresql://myuser:mypassword@{host}:{port}/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseManger:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w+")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
