import logging
import threading
import traceback

from flask import Flask, render_template, redirect
from flask_login import LoginManager
from typing import Union
from web.database.tables.users import Users
from .database.db_operator import DBOperator


logger: Union[logging.Logger, None] = None
db_operator: Union[DBOperator, None] = None


def create_api(flask_log: bool,
               logging_cgf_path: str,
               db_host: str,
               db_port: int,
               db_login: str,
               db_password: str,
               db_name: str
               ) -> Flask:
    global logger, db_operator

    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    count_module_to_connect = 3
    iteration_module = 1

    # Инициализация логирования
    from .init_logger import get_logger
    logger = get_logger(
        logging_cfg_path=logging_cgf_path,
        flask_log=flask_log,
        flask_app=app,
    )

    logger.info(f'[{iteration_module}/{count_module_to_connect}] Create logger: success')
    iteration_module += 1

    from .database import db_session

    # Инициализация Базы данных
    db_operator = DBOperator(
        logger=logger,
        db_host=db_host,
        db_port=db_port,
        db_login=db_login,
        db_password=db_password,
        db_name=db_name
    )

    app.config['SECRET_KEY'] = 'SECRET'

    @login_manager.user_loader
    def load_user(user_id):  # Возвращает информацию о пользователе по его ID
        s = db_session.create_session()
        return s.query(Users).get(user_id)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html")

    @app.route('/', methods=['GET'])
    def no_static():
        try:
            logger.debug(f'Redirect to static')
            return redirect('/static/monitoring')
        except Exception as e:
            logger.debug(traceback.format_exc())

    from . import endpoint_static_controllers as static_control
    from . import endpoint_ajax_controllers as ajax_control

    # Подключение endpoint`ов
    app.register_blueprint(static_control.module)
    logger.info(f'[{iteration_module}/{count_module_to_connect}] Connect static_endpoint: success')
    iteration_module += 1
    app.register_blueprint(ajax_control.module)
    logger.info(f'[{iteration_module}/{count_module_to_connect}] Connect ajax_endpoint: success')
    iteration_module += 1

    return app
