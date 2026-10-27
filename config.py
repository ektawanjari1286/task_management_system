import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "my-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///task_management.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False