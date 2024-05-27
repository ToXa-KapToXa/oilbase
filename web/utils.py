import random
import time
import traceback

from web import logger, db_operator


# Виды нефтепродуктов
oils = {
    'gasoline': 'Бензин',
    "diesel": 'Дизельное топливо',
    "masut": 'Мазут',
    "solar": 'Солярное масло',
    "kerosene": 'Керосин',
    '': '',
}

# Данные для таблицы Качества нефтепродуктов
quality = {
    'Бензин': {
        'density': '0,74',
        'viscosity': '33',
        'sulfur': '13',
    },
    "Дизельное топливо": {
        'density': '0,83',
        'viscosity': '24',
        'sulfur': '13',
    },
    "Мазут": {
        'density': '0,91',
        'viscosity': '45',
        'sulfur': '27',
    },
    "Солярное масло": {
        'density': '0,85',
        'viscosity': '37',
        'sulfur': '18',
    },
    "Керосин": {
        'density': '0,79',
        'viscosity': '29',
        'sulfur': '34',
    },
}

# Месяца для столбчатой диаграммы
months = {
    '01': 'Январь',
    '02': 'Февраль',
    '03': 'Март',
    '04': 'Апрель',
    '05': 'Май',
    '06': 'Июнь',
    '07': 'Июль',
    '08': 'Август',
    '09': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь'
}


def get_data():
    try:
        # Генерируем случайные значения
        reservoirs = db_operator.get_reservoirs()
        f_list = []
        t_list = []
        p_list = []
        gray_list = []
        p2_list = []
        t2_list = []
        levels_reservoirs = []
        purple_list = []
        yellow_list = []
        for i in range(len(reservoirs)):
            f_list.append(round(random.uniform(400, 600), 1))
            t_list.append(round(random.uniform(80, 120), 1))
            p_list.append(round(random.uniform(0, 3), 2))
            gray_list.append(round(random.uniform(0, 1), 2))
            p2_list.append(round(random.uniform(0, 3), 2))
            t2_list.append(round(random.uniform(80, 120), 1))
            levels_reservoirs.append(int(reservoirs[i]['fullness'] / reservoirs[i]['capacity'] * 100))
            purple_list.append(((round(random.uniform(0, 100), 1)), round(random.uniform(0, 100), 1)))

        for i in range(len(reservoirs) - 1):
            yellow_list.append(random.randint(0, 100))

        t_all_list = [round(random.uniform(80, 120), 1), round(random.uniform(80, 120), 1)]
        f_all_list = [round(random.uniform(400, 600), 1), round(random.uniform(400, 600), 1)]
        levels_reservoirs_all = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        info_list = [
            [random.randint(0, 100), round(random.uniform(0, 1000), 1), round(random.uniform(0, 30), 1)],
            [random.randint(0, 100), round(random.uniform(0, 1000), 1), round(random.uniform(0, 30), 1)],
        ]

        logger.debug(f'<UTILS.GET_DATA> Data for monitoring created!')

        # Запишем данные в БД
        db_operator.add_reservoir_data(reservoirs=reservoirs,
                                       f_list=f_list,
                                       t1_list=t_list,
                                       t2_list=t2_list,
                                       p1_list=p_list,
                                       p2_list=p2_list)

        return f_list, t_list, p_list, gray_list, p2_list, t2_list, levels_reservoirs, purple_list, t_all_list, f_all_list, levels_reservoirs_all, info_list, yellow_list
    except Exception as e:
        logger.debug(f'<<ERROR.UTILS>> Creating data for monitoring is Failed!')
        logger.error(traceback.format_exc())
