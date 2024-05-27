import sqlalchemy

from ..db_session import SqlAlchemyBase


class History(SqlAlchemyBase):
    __tablename__ = 'history'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Boolean)
    name = sqlalchemy.Column(sqlalchemy.Text)
