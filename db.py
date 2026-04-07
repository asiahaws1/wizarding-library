import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def init_db(app, database=None):
    database_client = database if database is not None else db
    database_uri = os.getenv("DATABASE_URI")
    if not database_uri:
        database_scheme = os.getenv("DATABASE_SCHEME")
        database_user = os.getenv("DATABASE_USER")
        database_password = os.getenv("DATABASE_PASSWORD", "")
        database_address = os.getenv("DATABASE_ADDRESS")
        database_port = os.getenv("DATABASE_PORT")
        database_name = os.getenv("DATABASE_NAME")
        if all([database_scheme, database_user, database_address, database_port, database_name]):
            if database_password:
                database_uri = (
                    f"{database_scheme}{database_user}:{database_password}"
                    f"@{database_address}:{database_port}/{database_name}"
                )
            else:
                database_uri = (
                    f"{database_scheme}{database_user}"
                    f"@{database_address}:{database_port}/{database_name}"
                )
        else:
            raise ValueError("Missing database environment variables")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database_client.init_app(app)
