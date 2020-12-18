import requests
from shared_utils.common.dt import dtf
from shared_utils.io.io import write, write_changed

import conf


def download_cist(groups, date_from, date_to, group_slug):
    url = f'https://cist.nure.ua/ias/app/tt/' \
          f'WEB_IAS_TT_GNR_RASP.GEN_GROUP_POTOK_RASP' \
          f'?ATypeDoc=3&Aid_group={groups}' \
          f'&Aid_potok=0&ADateStart={date_from}&ADateEnd={date_to}' \
          f'&AMultiWorkSheet=0'

    filename = f'{conf.data_path}/{group_slug}.csv'
    content = requests.get(url).content.decode('cp1251')
    if write_changed(filename, content):
        day_slug = dtf('Ymd')
        time_slug = dtf('dts')
        backup_filename = \
            f'{conf.data_path}/{day_slug}/{group_slug}_{time_slug}.csv'
        write(backup_filename, content)


if __name__ == '__main__':
    groups = '7706427_7999876_7706511_7706429_7985986_7985998_7706363_' \
             '7706315_7706393_7985980_7985982_7706507'
    download_cist(groups, '01.09.2020', '31.01.2021', 'pzpi-19')
