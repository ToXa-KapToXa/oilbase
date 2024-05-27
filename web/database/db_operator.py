import logging
import traceback
import datetime

from .db_session import global_init, create_session
from web.database.tables.users import Users
from web.database.tables.reservoirs import Reservoirs
from web.database.tables.history import History
from web.database.tables.reservoirs_data import ReservoirsData
from typing import Union
from sqlalchemy import desc


class DBOperator:
    def __init__(self, db_host, db_port, db_login, db_password, db_name, logger: logging.Logger):
        global_init(
            logger=logger,
            db_host=db_host,
            db_port=db_port,
            db_login=db_login,
            db_password=db_password,
            db_name=db_name
        )
        self.logger = logger
        self.logger.debug(f'<DB_OPERATOR> DB_Operator is initialized!')

    def auth(self, login: str,
             password: str):
        try:
            session = create_session()
            some_user = session.query(Users).filter(Users.login == login, Users.password == password).first()
            session.close()
            if some_user is not None:
                self.logger.debug(f'<DB_OPERATOR> User is founded!')
                return True, some_user
            self.logger.debug(f'<DB_OPERATOR> User is NOT founded!')
            return False, None
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Auth is failed!')
            self.logger.error(traceback.format_exc())

    def get_reservoirs(self) -> list:
        try:
            session = create_session()
            reservoirs = session.query(Reservoirs).all()
            session.close()
            list_reservoirs = []
            for reservoir in reservoirs:
                dict_reservoirs = {
                    'id': reservoir.id,
                    'include': reservoir.include,
                    'pressure': reservoir.pressure,
                    'capacity': reservoir.capacity,
                    'fullness': reservoir.fullness,
                    'name': reservoir.name,
                }
                list_reservoirs.append(dict_reservoirs)
            self.logger.debug(f'<DB_OPERATOR> Getting reserviors is success!')
            return list_reservoirs
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Getting reservoirs is Failed!')
            self.logger.error(traceback.format_exc())

    def add_reservoir(self, name: str,
                      pressure: str,
                      capacity: int,
                      include: Union[str, None] = None,
                      fullness: Union[int, None] = None,):
        try:
            self.logger.debug(f'<DB_OPERATOR> Creating new reservoir')
            session = create_session()
            new_reservoir = Reservoirs(
                name=name,
                include=include,
                pressure=pressure,
                capacity=capacity,
                fullness=fullness
            )
            if fullness:
                new_history = History(
                    name=include,
                    count=fullness,
                    type=True,
                    date=datetime.date.today()
                )
                session.add(new_history)
            session.add(new_reservoir)
            session.commit()
            session.close()
            self.logger.debug(f"<DB_OPERATOR> Adding new reservoir: {name} is success")
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Creating new reservoir: {name} is Failed!')
            self.logger.error(traceback.format_exc())

    def update_reservoir(self, reservoir_id: int,
                         name: str,
                         pressure: str,
                         capacity: int,
                         include: Union[str, None] = None,
                         fullness: Union[int, None] = None,):
        try:
            session = create_session()
            reservoir = session.query(Reservoirs).filter_by(id=reservoir_id).first()
            if reservoir:
                reservoir.name = name,
                reservoir.pressure = pressure
                reservoir.capacity = capacity
                if reservoir.include != include:
                    new_history = History(
                        name=reservoir.include,
                        count=reservoir.fullness,
                        type=False,
                        date=datetime.date.today()
                    )
                    session.add(new_history)
                    new_history = History(
                        name=include,
                        count=fullness,
                        type=True,
                        date=datetime.date.today()
                    )
                    session.add(new_history)
                elif reservoir.fullness != fullness:
                    if int(reservoir.fullness) > int(fullness):
                        new_history = History(
                            name=reservoir.include,
                            count=int(reservoir.fullness) - int(fullness),
                            type=False,
                            date=datetime.date.today()
                        )
                        session.add(new_history)
                    else:
                        new_history = History(
                            name=reservoir.include,
                            count=int(fullness) - int(reservoir.fullness),
                            type=True,
                            date=datetime.date.today()
                        )
                        session.add(new_history)
                reservoir.include = include
                reservoir.fullness = fullness
                session.commit()
            session.close()
            self.logger.debug(f"<DB_OPERATOR> Updating the reservoir: {name} is success")
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Updating reservoir is Failed!')
            self.logger.error(traceback.format_exc())

    def delete_reservoir_by_id(self, reservoir_id: int):
        try:
            session = create_session()
            reservoir = session.query(Reservoirs).filter_by(id=reservoir_id).first()
            session.delete(reservoir)
            session.commit()
            session.close()
            self.logger.debug(f'<DB_OPERATOR> Reservoir is success deleted!')
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Deleting reservoir is Failed!')
            self.logger.error(traceback.format_exc())

    def get_reservoir_by_id(self, reservoir_id: int):
        try:
            session = create_session()
            reservoir = session.query(Reservoirs).filter_by(id=reservoir_id).first()
            session.close()
            if reservoir:
                self.logger.debug(f"<DB_OPERATOR> The reservoir with id {reservoir_id}: {reservoir.name} is founded!")
                return reservoir
            else:
                self.logger.debug(f"<DB_OPERATOR> The reservoir with id {reservoir_id} is NOT founded!")
                return None
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Getting reservoir by id={reservoir_id} is Failed!')
            self.logger.error(traceback.format_exc())

    def get_history(self):
        try:
            session = create_session()
            history = session.query(History).all()
            session.close()
            if history:
                self.logger.debug(f'<DB_OPERATOR> Getting history is success!')
                return history
            else:
                self.logger.debug(f'<DB_OPERATOR> Getting history is NOT success!')
                return None
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Getting history is Failed!')
            self.logger.error(traceback.format_exc())

    def get_history_by_date(self, start_date, end_date):
        try:
            session = create_session()
            history = session.query(History).filter(History.date >= start_date).filter(History.date <= end_date).all()
            session.close()
            if history:
                self.logger.debug(f'<DB_OPERATOR> Getting history by date is success!')
                return history
            else:
                self.logger.debug(f'<DB_OPERATOR> Getting history by date is NOT success!')
                return None
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Getting history by date is Failed!')
            self.logger.error(traceback.format_exc())

    def add_reservoir_data(self, reservoirs, f_list, t1_list, t2_list, p1_list, p2_list):
        try:
            self.logger.debug(f'<DB_OPERATOR> Creating new reservoirs_data')
            session = create_session()
            for i in range(len(reservoirs)):
                new_reservoir_data = ReservoirsData(
                    reservoir_id=reservoirs[i]['id'],
                    f=f_list[i],
                    t1=t1_list[i],
                    t2=t2_list[i],
                    p1=p1_list[i],
                    p2=p2_list[i],
                    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                session.add(new_reservoir_data)
                session.commit()
            session.close()
            self.logger.debug(f"<DB_OPERATOR> Adding new reservoirs_data is success")
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Adding reservoir_data is Failed!')
            self.logger.error(traceback.format_exc())

    def get_reservoir_data_by_reservoir_id(self, reservoir_id):
        try:
            session = create_session()
            reservoirs_data = session.query(ReservoirsData).filter_by(reservoir_id=reservoir_id).order_by(desc(ReservoirsData.date)).limit(5).all()
            session.close()
            return reservoirs_data
        except Exception as e:
            self.logger.debug(f'<<ERROR.DB_OPERATOR>> Getting reservoir_data is Failed!')
            self.logger.error(traceback.format_exc())
