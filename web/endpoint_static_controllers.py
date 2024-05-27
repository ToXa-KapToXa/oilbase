import openpyxl
import datetime
import os
from flask import Blueprint, render_template, request, redirect, send_file
from flask_login import login_user, logout_user, login_required, current_user

from web.utils import *

module = Blueprint(name='statics_page', import_name=__name__, url_prefix='/static')


######################
# Страница мониторинга
@module.route('/monitoring', methods=['GET', 'POST'])
def index():
    try:
        # Аутентификация
        # Если пользователь не авторизован, то перенаправляем на страницу авторизации
        if not current_user.is_authenticated:
            return redirect("/static/login")

        # Генерируем случайные числа
        f_list, t_list, p_list, gray_list, p2_list, t2_list, levels_reservoirs, purple_list, t_all_list, f_all_list, levels_reservoirs_all, info_list, yellow_list = get_data()

        return render_template('monitoring.html',
                               current_menu='monitoring',
                               title='Мониторинг',
                               f_list=f_list,
                               t_list=t_list,
                               p_list=p_list,
                               gray_list=gray_list,
                               p2_list=p2_list,
                               t2_list=t2_list,
                               levels_reservoirs=levels_reservoirs,
                               purple_list=purple_list,
                               t_all_list=t_all_list,
                               f_all_list=f_all_list,
                               levels_reservoirs_all=levels_reservoirs_all,
                               info_list=info_list,
                               yellow_list=yellow_list,
                               )
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with index!')
        logger.error(traceback.format_exc())


####################
# Страница аналитики
@module.route('/analyze', methods=['GET', 'POST'])
def analyze():
    try:
        # Аутентификация
        # Если пользователь не авторизован, то перенаправляем на страницу авторизации
        if not current_user.is_authenticated:
            return redirect("/static/login")

        # Получаем резервуары
        reservoirs = db_operator.get_reservoirs()

        # Круговая диаграмма
        doughnut_total = 0
        labels_and_counts = {}
        for reservoir in reservoirs:
            if reservoir['fullness'] > 0:
                if not labels_and_counts.get(oils[reservoir['include']], False):
                    labels_and_counts[oils[reservoir['include']]] = 0
                labels_and_counts[oils[reservoir['include']]] += reservoir['fullness']
                doughnut_total += reservoir['fullness']

        # Таблица данных резервуаров
        data_table = []
        reservoir_id = reservoirs[0]['id']
        reservoir_name = reservoirs[0]['name']
        if not request.form.get('choose_reservoir_data', '!!!') != '!!!':
            # Получаем список изменений
            reservoirs_data = db_operator.get_reservoir_data_by_reservoir_id(reservoir_id=reservoir_id)
            for reservoir_data in reservoirs_data:
                jsn = {
                    'date': reservoir_data.date,
                    'f': reservoir_data.f,
                    't1': reservoir_data.t1,
                    't2': reservoir_data.t2,
                    'p1': reservoir_data.p1,
                    'p2': reservoir_data.p2
                }
                data_table.append(jsn)

        # Столбчатая диаграмма
        history = db_operator.get_history()
        months_and_counts = {}

        for i in history:
            date = i.date.strftime('%Y/%m/%d')
            if not months_and_counts.get(months[date.split('/')[1]], False):
                months_and_counts[months[date.split('/')[1]]] = [0, 0]
            if i.type:
                months_and_counts[months[date.split('/')[1]]][0] += i.count
            else:
                months_and_counts[months[date.split('/')[1]]][1] += i.count

        # Если нажали на кнопку
        if request.method == 'POST':
            # Если создаем отчет
            if request.form.get('create_report', '!!!') != '!!!':
                start_date = request.form.get('trip-start', '')
                end_date = request.form.get('trip-end', '')

                # Путь для создания файла
                file_path = 'web/files/data.xlsx'
                # Проверяем наличие файла
                if os.path.exists(file_path):
                    # Если файл существует, удаляем его
                    os.remove(file_path)
                    logger.debug(f"File {file_path} success deleted!")
                else:
                    logger.debug(f"File {file_path} is NOT exist!")

                # Получаем историю по дате
                history = db_operator.get_history_by_date(start_date=start_date,
                                                          end_date=end_date)
                # Создаем новую книгу (Excel файл)
                workbook = openpyxl.Workbook()
                # Выбираем активный лист
                sheet = workbook.active

                # Записываем данные в ячейки
                sheet['A1'] = 'Продукт'
                sheet['B1'] = 'Количество, тонна'
                sheet['C1'] = 'Тип'
                sheet['D1'] = 'Дата'
                count = 2
                for hist in history:
                    sheet[f'A{count}'] = oils[hist.name]
                    sheet[f'B{count}'] = hist.count
                    sheet[f'C{count}'] = 'Поступление' if hist.type else 'Отгрузка'
                    sheet[f'D{count}'] = str(hist.date.strftime('%Y/%m/%d'))
                    count += 1

                # Сохраняем книгу в файл
                workbook.save(file_path)

                return send_file('files\\data.xlsx', as_attachment=True)

            # Если выбрали резервуар
            if request.form.get('choose_reservoir_data', '!!!') != '!!!':
                chosen_reservoir_data = request.form.get('reservoir_data', '')
                reservoir_id = chosen_reservoir_data.split('_')[0]
                reservoir_name = chosen_reservoir_data.split('_')[1]
                # Получаем список изменений
                reservoirs_data = db_operator.get_reservoir_data_by_reservoir_id(reservoir_id=reservoir_id)
                for reservoir_data in reservoirs_data:
                    jsn = {
                        'date': reservoir_data.date,
                        'f': reservoir_data.f,
                        't1': reservoir_data.t1,
                        't2': reservoir_data.t2,
                        'p1': reservoir_data.p1,
                        'p2': reservoir_data.p2
                    }
                    data_table.append(jsn)

        logger.debug(f'{data_table=}')

        return render_template('analyze.html',
                               current_menu='analyze',
                               title='Аналитика',
                               doughnut_data=list(labels_and_counts.values()),
                               doughnut_labels=list(labels_and_counts.keys()),
                               doughnut_total=doughnut_total,
                               reservoirs=reservoirs,
                               data_table=data_table,
                               diagram_labels=list(months_and_counts.keys())[-6:],
                               diagram_data_in=[i[0] for i in list(months_and_counts.values())][-6:],
                               diagram_data_out=[i[1] for i in list(months_and_counts.values())][-6:],
                               today_date=datetime.date.today(),
                               chosen_reservoir=reservoir_name)
    except Exception as e:
        logger.error(traceback.format_exc())


####################
# Страница настройки
@module.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        # Аутентификация
        # Если пользователь не авторизован, то перенаправляем на страницу авторизации
        if not current_user.is_authenticated:
            return redirect("/static/login")

        # Получаем информацию о резервуарах
        reservoirs = db_operator.get_reservoirs()

        # Если нажали на кнопку
        if request.method == 'POST':
            logger.debug(f'<PAGE.SETTINGS> POST: {request.form}')
            # Если нажали на кнопку добавления резервуара
            if request.form.get('add_reservoir', False):
                # Перенаправляем на эндпоинт добавления резервуара
                return redirect('/static/add_reservoir')

        return render_template('settings.html',
                               current_menu='settings',
                               title='Настройка',
                               reservoirs=reservoirs,
                               oils=oils)
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with settings!')
        logger.error(traceback.format_exc())


################################
# Страница добавления резервуара
@module.route('/add_reservoir', methods=['GET', 'POST'])
def add_reservoir():
    try:
        # Аутентификация
        # Если пользователь не авторизован, то перенаправляем на страницу авторизации
        if not current_user.is_authenticated:
            return redirect("/static/login")

        # Если нажали на кнопку
        if request.method == 'POST':
            logger.debug(f'<PAGE.ADD_RESERVOIR> POST: {request.form}')
            # Если нажали на кнопку добавления резервуара
            if request.form.get('button_add_reservoir', '!!!') != '!!!':
                # Считываем поля
                name = request.form.get('name_of_reservoir', False)
                capacity = request.form.get('capacity', False)
                pressure = request.form.get('pressure', False)
                fullness = request.form.get('fullness', False)
                if not fullness:
                    fullness = 0
                include = request.form.get('include', False)
                # Добавляем резервуар
                db_operator.add_reservoir(name=name,
                                          capacity=capacity,
                                          pressure=pressure,
                                          fullness=fullness,
                                          include=include)
                # Перенаправляем на страницу настройки
                return redirect('/static/settings')

        return render_template('add_reservoir.html',
                               current_menu='add_reservoir',
                               title='Добавление резервуара', )
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with adding the reservoir!')
        logger.error(traceback.format_exc())


####################################
# Страница редактирования резервуара
@module.route('/edit_reservoir/<int:reservoir_id>', methods=['GET', 'POST'])
def edit_reservoir(reservoir_id: int):
    try:
        # Аутентификация
        # Если пользователь не авторизован, то перенаправляем на страницу авторизации
        if not current_user.is_authenticated:
            return redirect("/static/login")

        # Получаем информацию о резервуаре по его ID
        reservoir = db_operator.get_reservoir_by_id(reservoir_id=reservoir_id)

        # Если нажали на кнопку
        if request.method == 'POST':
            logger.debug(f'<PAGE.EDIT_RESERVOIR> POST: {request.form}')
            # Если нажали на кнопку добавления резервуара
            if request.form.get('button_edit_reservoir', '!!!') != '!!!':
                # Считываем поля
                name = request.form.get('name_of_reservoir', False)
                capacity = request.form.get('capacity', False)
                pressure = request.form.get('pressure', False)
                fullness = request.form.get('fullness', False)
                if not fullness:
                    fullness = 0
                include = request.form.get('include', False)
                # Обновляем информацию о резервуаре
                db_operator.update_reservoir(reservoir_id=reservoir_id,
                                             name=name,
                                             capacity=capacity,
                                             pressure=pressure,
                                             fullness=fullness,
                                             include=include)
                # Перенаправляем на страницу настройки
                return redirect('/static/settings')

        return render_template('edit_reservoir.html',
                               current_menu='edit_reservoir',
                               title='Изменение резервуара',
                               reservoir=reservoir,
                               oil_translate=oils[reservoir.include])
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with editing the reservoir!')
        logger.error(traceback.format_exc())


##############################
# Страница удаления резервуара
@module.route('/delete_reservoir/<int:reservoir_id>', methods=['GET', 'POST'])
def delete_reservoir(reservoir_id: int):
    try:
        # Удаляем резервуар по его ID
        db_operator.delete_reservoir_by_id(reservoir_id=reservoir_id)
        return redirect('/static/settings')
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with deleting the reservoir!')
        logger.error(traceback.format_exc())


######################
# СТРАНИЦА АВТОРИЗАЦИЯ
@module.route("/login", methods=['GET', 'POST'])
def login():
    try:
        # Если пользователь авторизован
        if current_user.is_authenticated:
            return redirect("/static/monitoring")

        if request.method == 'POST':
            rem = request.form.get("remember", False)
            if rem == "on":
                rem = True
            else:
                rem = False

            is_success, user = db_operator.auth(login=request.form.get('login', '-'),
                                                password=request.form.get('password', '-'))
            if is_success:
                login_user(user, remember=rem)
                return redirect("/static/monitoring")

            return render_template('login.html',
                                   message="*Неправильный логин или пароль")
        return render_template('login.html',
                               message=False)
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with authorisation user!')
        logger.error(traceback.format_exc())


##################
# СТРАНИЦА ЛОГАУТА
@module.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        return redirect('/static/login')
    except Exception as e:
        logger.debug(f'<ENDPOINT.STATIC> Error with logout user!')
        logger.error(traceback.format_exc())
