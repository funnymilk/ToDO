from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ToDo App"
    DEBUG: bool = True

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        #url = f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        url = "postgresql+psycopg://todo:secret@localhost:5433/todo_db"
        return url

    class Config:
        env_file = ".env"
