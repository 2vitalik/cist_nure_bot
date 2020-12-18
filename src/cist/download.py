import requests
from shared_utils.io.io import write, write_changed

import conf
from src.utils.filename import get_filenames
from src.utils.slack import slack_status


def download_cist(groups, date_from, date_to, group_slug):
    url = f'https://cist.nure.ua/ias/app/tt/' \
          f'WEB_IAS_TT_GNR_RASP.GEN_GROUP_POTOK_RASP' \
          f'?ATypeDoc=3&Aid_group={groups}' \
          f'&Aid_potok=0&ADateStart={date_from}&ADateEnd={date_to}' \
          f'&AMultiWorkSheet=0'

    content = requests.get(url).content.decode('cp1251').replace('\r', '\n')

    path = f'{conf.data_path}/cist'
    active_filename, backup_filename = get_filenames(path, group_slug, 'csv')

    if write_changed(active_filename, content):
        slack_status(f'cist changed: csv')
        write(backup_filename, content)


if __name__ == '__main__':
    groups = '7706427_7999876_7706511_7706429_7985986_7985998_7706363_' \
             '7706315_7706393_7985980_7985982_7706507'
    download_cist(groups, '01.09.2020', '31.01.2021', 'pzpi-19')
