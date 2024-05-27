import sqlalchemy

from ..db_session import SqlAlchemyBase


class Reservoirs(SqlAlchemyBase):
    __tablename__ = 'reservoirs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    include = sqlalchemy.Column(sqlalchemy.Text)
    pressure = sqlalchemy.Column(sqlalchemy.Text)
    capacity = sqlalchemy.Column(sqlalchemy.Integer)
    fullness = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.Text)
