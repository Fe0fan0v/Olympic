import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Team(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teams'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.String)
    scores = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    position = sqlalchemy.Column(sqlalchemy.Integer, default=0)
