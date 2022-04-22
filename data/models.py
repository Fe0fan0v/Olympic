import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType


class Team(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teams'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.String)
    deadline = sqlalchemy.Column(MutableList.as_mutable(PickleType), default=None)
    timer_started = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    scores = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    position = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    tasks_done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    first_block_answer = sqlalchemy.Column(sqlalchemy.String, default=None)
    second_block_answer = sqlalchemy.Column(sqlalchemy.String, default=None)
    third_block_answer = sqlalchemy.Column(sqlalchemy.String, default=None)
    fourth_block_answer = sqlalchemy.Column(sqlalchemy.String, default=None)
    final_block_answer = sqlalchemy.Column(sqlalchemy.String, default=None)
    last_answer = sqlalchemy.Column(sqlalchemy.DATETIME, default=None)
