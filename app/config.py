import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    def __init__(self) -> None:
        self.db_name = os.environ.get('DB_NAME')
        self.db_pass = os.environ.get('DB_PASS')
        self.db_host = os.environ.get('DB_HOST')
        self.db_user = os.environ.get('DB_USER')
        self.db_port = os.environ.get('DB_PORT')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_uri = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        return db_uri