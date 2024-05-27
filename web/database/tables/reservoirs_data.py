import sqlalchemy

from ..db_session import SqlAlchemyBase


class ReservoirsData(SqlAlchemyBase):
    __tablename__ = 'reservoirs_data'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    reservoir_id = sqlalchemy.Column(sqlalchemy.Integer)
    f = sqlalchemy.Column(sqlalchemy.Text)
    t1 = sqlalchemy.Column(sqlalchemy.Text)
    t2 = sqlalchemy.Column(sqlalchemy.Text)
    p1 = sqlalchemy.Column(sqlalchemy.Text)
    p2 = sqlalchemy.Column(sqlalchemy.Text)
    date = sqlalchemy.Column(sqlalchemy.Text)
