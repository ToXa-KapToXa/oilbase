from web import create_api
from configs.settings import *


app = create_api(
    flask_log=FLASK_LOG,
    logging_cgf_path=LOGGING_CFG_PATH,
    db_host=DB_HOST,
    db_port=DB_PORT,
    db_login=DB_LOGIN,
    db_password=DB_PASSWORD,
    db_name=DB_NAME,
)

if __name__ == '__main__':
    app.run(
        host=HOST_SERVER,
        port=PORT_SERVER,
        debug=True
    )
