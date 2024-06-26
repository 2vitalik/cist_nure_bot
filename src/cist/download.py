import traceback

import requests
from shared_utils.common.dt import dtf
from shared_utils.io.io import write, write_changed

import conf
from src.utils.filename import get_filenames
from src.utils.slack import slack_status


def download_cist(groups, date_from, date_to, potok_slug):
    path = f'{conf.data_path}/cist'

    url = f'https://cist.nure.ua/ias/app/tt/' \
          f'WEB_IAS_TT_GNR_RASP.GEN_GROUP_POTOK_RASP' \
          f'?ATypeDoc=3&Aid_group={groups}' \
          f'&Aid_potok=0&ADateStart={date_from}&ADateEnd={date_to}' \
          f'&AMultiWorkSheet=0'

    try:
        content = \
            requests.get(url).content.decode('cp1251').replace('\r', '\n')
    except requests.exceptions.ConnectionError as e:
        time_slug = dtf('dts')
        error_filename = f'{path}/errors/{potok_slug}__{time_slug}.csv'
        write(error_filename, traceback.format_exc().strip())
        if 'Max retries exceeded' in f'{e}':
            slack_status(f'⚠️ cist.nure.ua вернул ошибку для'
                         f' `{potok_slug}`: Max retries exceeded')
        else:
            slack_status(f'⚠️ cist.nure.ua вернул ошибку для'
                         f' `{potok_slug}`: *{type(e).__name__}*: {e}')
        return False

    active_filename, backup_filename = get_filenames(path, potok_slug, 'csv')

    error_patterns = [
        'Запрашиваемый документ в разработке',
        'Service Temporarily Unavailable',
        '502 Bad Gateway',
    ]
    for error_pattern in error_patterns:
        if error_pattern in content:
            time_slug = dtf('dts')
            error_filename = f'{path}/errors/{potok_slug}__{time_slug}.csv'
            write(error_filename, content)
            slack_status(f'⚠️ cist.nure.ua вернул ошибку для'
                         f' `{potok_slug}`: *"{error_pattern}"*')
            return False

    if write_changed(active_filename, content):
        slack_status(f'✔️ *cist/csv* data has changed for `{potok_slug}`')
        write(backup_filename, content)

    return True


if __name__ == '__main__':
    groups = '7706427_7999876_7706511_7706429_7985986_7985998_7706363_' \
             '7706315_7706393_7985980_7985982_7706507'
    download_cist(groups, '01.09.2020', '31.01.2021', 'pzpi-19')
