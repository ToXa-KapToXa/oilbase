import traceback
from flask import Blueprint, render_template, request, jsonify

from . import logger
from web.utils import get_data


module = Blueprint(name='ajax_page', import_name=__name__, url_prefix='/ajax')


@module.route('/get_data_for_monitoring', methods=['GET'])
def get_data_for_monitoring():
    try:
        input_data = request.form
        logger.debug(f'<AJAX> {input_data=}')
        # Генерируем случайные числа
        f_list, t_list, p_list, gray_list, p2_list, t2_list, levels_reservoirs, purple_list, t_all_list, f_all_list, levels_reservoirs_all, info_list, yellow_list = get_data()

        return jsonify({'data': render_template(
            "ajax/monitoring.html",
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
        )})
    except Exception as e:
        logger.debug(f'<ENDPOINT.AJAX> Error with getting data for monitoring!')
        logger.error(traceback.format_exc())


