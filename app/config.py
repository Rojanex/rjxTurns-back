import os

class Config:
    def __init__(self) -> None:
        self.db_name = os.environ.get('DB_NAME')
        self.db_pass = os.environ.get('DB_PASS')
        self.db_host = os.environ.get('DB_HOST')
        self.db_user = os.environ.get('DB_USER')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"