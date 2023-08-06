"""Module for accessing to databases.
"""
import json
import sys
from pathlib import Path

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from pymysql import cursors, connect, OperationalError

db = SQLAlchemy()

Base = declarative_base()


def init_db(app):
    db.init_app(app)


class DBInit():
    """Initializing database to save user's accounts.
    """

    def __init__(
            self, username: str = "root", password: str = None,
            host: str = "localhost", port: int = 3306):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = 'raspi'

    def read_json(self, js: str):
        with open(js, "r") as f:
            d = json.load(f)
        self.username = d["username"]
        self.password = d["password"]
        self.host = d["server"]
        self.port = d["port"]
        self.db_name = d["db_name"]

    def db_setup(self):
        self.create_database()
        self.create_table()
        self.add_admin()

    def create_database(self):
        """Creates new database.

        The database named "raspi" is created with mysql.
        """
        try:
            engine = create_engine(f"mysql://{self.username}:{self.password}@{self.host}:{self.port}")
            with engine.connect() as conn:
                conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        except:
            raise

    def create_table(self):
        """Creates new table if not exist.

        The table named 'user' to store information about user's account is created in the
        database.
        """
        engine = create_engine(f"mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.db_name}?charset=utf8")
        Base.metadata.create_all(bind=engine)
        print("\033[34mCreate 'user' table in database 'raspi'\033[0m")

    def add_admin(self):
        """Adds an admin user if not exist.

        Adds the user if not exist in the table. The user is

            - Username : admin
            - Password : admin
            - User ID : 000
        """
        engine = create_engine(f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}?charset=utf8")
        SessionClass = sessionmaker(engine)
        session = SessionClass()
        user = session.query(User2).filter_by(username="admin").first()
        if user:
            print("\033[31mUser 'admin' already exists.\033[0m")
            return False
        user = User2(user_id="000", username="admin")
        user.password = Bcrypt().generate_password_hash("admin").decode('utf-8')
        session.add(user)
        session.commit()
        print("\033[34mCreate admin user.\033[0m")
        return True

    def delete_database(self):
        f = Path(__file__).resolve().parent / "config/database.json"
        self.read_json(str(f))
        cursor_type = cursors.DictCursor
        connection = connect(
            host=self.host,
            user=self.username,
            password=self.password,
            cursorclass=cursor_type)
        db_curse = connection.cursor()
        sql = f"drop database {self.db_name}"
        try:
            db_curse.execute(sql)
            print(f"Deleted {self.db_name} database")
            print("Database delete sucessfully completed.")
        except OperationalError:
            print("Database delete failed.", file=sys.stderr)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.String, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "User('{}')".format(self.username)


class User2(Base):
    __tablename__ = "user"
    user_id = Column(String(100), primary_key=True, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


