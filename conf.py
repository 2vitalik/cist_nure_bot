from pathlib import Path

coda_token = None  # should be set in `local_conf.py`
coda_doc = None  # should be set in `local_conf.py`

telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`

mongo_cluster_secret = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

semester = '2025-1'
mongo_semester = '2025-p1'
date_from = '01.02.2025'
date_to = '01.08.2025'

google_chat_webhook = None  # should be set in `local_conf.py`

temporary_disable_tg = False
temporary_disable_slack_new = False

groups = {
    'pzpi-24': '11412125_11412139_11412127_11412129_11412133_11412135_11412131_'
               '11412137',
    'pzpi-23': '10887362_10887378_10887382_10887384_11103296_10887386_'
               '10887388_10887390_10887393_10887396',
    'pzpi-22': '10284307_10284309_10284313_10284311_10537885_10284315_'
               '10284317_10284319_10284321_10537887',
    'pzpi-21': '9291668_9291670_9291672_9291674_9291676_9291678_9291680_'
               '9291682_9291684_9291686_9291688',
    # 'pzpi-20': '8476596_8476506_8476548_8476618_8744039_8476450_8476364_'
    #            '8476408_8476572_8744041_8832021',
    # 'pzpi-19': '7706427_7999876_7706511_7706429_7985986_7985998_7706363_'
    #            '7706315_7706393_7985980_7985982_7706507',
    # 'pzpi-18': '6949772_7240401_6949830_6949706_6949774_7195531_6949688_'
    #            '6949724_6949726_6949654_7195529_7195533',
    # 'pzpi-17': '6283365_6283375_6496576_6496579_6283463_6283489_6283409_'
    #            '6496585_6496598_7197629_6569333',

    # 'ipzm-22': '10284301_10284303_10539519_10539521_10539523_10539525_10539534',
    'ipzm-23': '10887409_10887672_11104699_11104701',
    'ipzm-24': '11412141_11412143_11446248',
    'infm-24': '11416917_11416919',
    'knm-24': '11417173_11417175_11607882_11417167_11417169_11417177_11607884_11417171',
}

group_nums = {
    'ПЗПІ-24': {
        'max_eng_group': 3,
        'max_ukr_group': 7,
    },
    'ПЗПІ-23': {
        'max_eng_group': 5,
        'max_ukr_group': 10,
    },
    'ПЗПІ-22': {
        'max_eng_group': 5,
        'max_ukr_group': 10,
    },
    'ПЗПІ-21': {
        'max_eng_group': 5,
        'max_ukr_group': 11,
    },
    # 'ПЗПІ-20': {
    #     'max_eng_group': 5,
    #     'max_ukr_group': 10,
    # },
}

group_eng = {  # todo: auto-calculate by above?
    'ПЗПІ-24-1': True,
    'ПЗПІ-24-2': True,
    'ПЗПІ-24-3': True,
    'ПЗПІ-24-4': False,
    'ПЗПІ-24-5': False,
    'ПЗПІ-24-6': False,
    'ПЗПІ-24-7': False,

    'ПЗПІ-23-1': True,
    'ПЗПІ-23-2': True,
    'ПЗПІ-23-3': True,
    'ПЗПІ-23-4': True,
    'ПЗПІ-23-5': True,
    'ПЗПІ-23-6': False,
    'ПЗПІ-23-7': False,
    'ПЗПІ-23-8': False,
    'ПЗПІ-23-9': False,
    'ПЗПІ-23-10': False,

    'ПЗПІ-22-1': True,
    'ПЗПІ-22-2': True,
    'ПЗПІ-22-3': True,
    'ПЗПІ-22-4': True,
    'ПЗПІ-22-5': True,
    'ПЗПІ-22-6': False,
    'ПЗПІ-22-7': False,
    'ПЗПІ-22-8': False,
    'ПЗПІ-22-9': False,
    'ПЗПІ-22-10': False,

    # 'ІПЗм-22-1': True,
    # 'ІПЗм-22-2': True,
    # 'ІПЗм-22-3': True,
    # 'ІПЗм-22-4': True,
    # 'ІПЗм-22-5': True,
    # 'ІПЗм-22-6': True,
    # 'ІПЗм-22-7': True,

    'ІПЗм-23-1': True,
    'ІПЗм-23-2': True,
    'ІПЗм-23-3': True,
    'ІПЗм-23-4': True,

    'ІПЗм-24-1': True,
    'ІПЗм-24-2': True,
    'ІПЗм-24-3': True,

    'ПЗПІ-21-1': True,
    'ПЗПІ-21-2': True,
    'ПЗПІ-21-3': True,
    'ПЗПІ-21-4': True,
    'ПЗПІ-21-5': True,
    'ПЗПІ-21-6': False,
    'ПЗПІ-21-7': False,
    'ПЗПІ-21-8': False,
    'ПЗПІ-21-9': False,
    'ПЗПІ-21-10': False,
    'ПЗПІ-21-11': False,

    # 'ПЗПІ-20-1': True,
    # 'ПЗПІ-20-2': True,
    # 'ПЗПІ-20-3': True,
    # 'ПЗПІ-20-4': True,
    # 'ПЗПІ-20-5': True,
    # 'ПЗПІ-20-6': False,
    # 'ПЗПІ-20-7': False,
    # 'ПЗПІ-20-8': False,
    # 'ПЗПІ-20-9': False,
    # 'ПЗПІ-20-10': False,
    # 'ПЗПІи-20-1': False,
    #
    # 'ПЗПІ-19-1': True,
    # 'ПЗПІ-19-2': True,
    # 'ПЗПІ-19-3': True,
    # 'ПЗПІ-19-4': True,
    # 'ПЗПІ-19-5': True,
    # 'ПЗПІ-19-6': False,
    # 'ПЗПІ-19-7': False,
    # 'ПЗПІ-19-8': False,
    # 'ПЗПІ-19-9': False,
    # 'ПЗПІ-19-10': False,
    # 'ПЗПІ-19-11': False,
    # 'ПЗПІи-19-1': False,
    #
    # 'ПЗПІ-18-1': True,
    # 'ПЗПІ-18-2': True,
    # 'ПЗПІ-18-3': True,
    # 'ПЗПІ-18-4': True,
    # 'ПЗПІ-18-5': True,
    # 'ПЗПІ-18-6': False,
    # 'ПЗПІ-18-7': False,
    # 'ПЗПІ-18-8': False,
    # 'ПЗПІ-18-9': False,
    # 'ПЗПІ-18-10': False,
    # 'ПЗПІ-18-11': False,
    # 'ПЗПІи-18-1': False,
}

cist_ids = {
    'ПЗПІ-24-1': '11412125',
    'ПЗПІ-24-2': '11412127',
    'ПЗПІ-24-3': '11412129',
    'ПЗПІ-24-4': '11412131',
    'ПЗПІ-24-5': '11412133',
    'ПЗПІ-24-6': '11412135',
    'ПЗПІ-24-7': '11412137',
    # 'ПЗПІ-24-8': '11412139',

    'ПЗПІ-23-1': '10887362',
    'ПЗПІ-23-2': '10887378',
    'ПЗПІ-23-3': '10887382',
    'ПЗПІ-23-4': '10887384',
    'ПЗПІ-23-5': '11103296',
    'ПЗПІ-23-6': '10887386',
    'ПЗПІ-23-7': '10887388',
    'ПЗПІ-23-8': '10887390',
    'ПЗПІ-23-9': '10887393',
    'ПЗПІ-23-10': '10887396',

    'ПЗПІ-22-1': '10284307',
    'ПЗПІ-22-2': '10284309',
    'ПЗПІ-22-3': '10284313',
    'ПЗПІ-22-4': '10284311',
    'ПЗПІ-22-5': '10537885',
    'ПЗПІ-22-6': '10284315',
    'ПЗПІ-22-7': '10284317',
    'ПЗПІ-22-8': '10284319',
    'ПЗПІ-22-9': '10284321',
    'ПЗПІ-22-10': '10537887',

    # 'ІПЗм-22-1': '10284301',
    # 'ІПЗм-22-2': '10284303',
    # 'ІПЗм-22-3': '10539519',
    # 'ІПЗм-22-4': '10539521',
    # 'ІПЗм-22-5': '10539523',
    # 'ІПЗм-22-6': '10539525',
    # 'ІПЗм-22-7': '10539534',

    'ІПЗм-23-1': '10887409',
    'ІПЗм-23-2': '10887672',
    'ІПЗм-23-3': '11104699',
    'ІПЗм-23-4': '11104701',

    'ІПЗм-24-1': '11412141',
    'ІПЗм-24-2': '11412143',
    'ІПЗм-24-3': '11446248',

    'ІТПм-24-1': '11417175',
    'ІТПм-24-2': '11607882',
    'ІУСТм-24-1': '11417173',
    'СПРм-24-1': '11417171',
    'УПГІТм-24-1': '11417167',
    'СШІм-24-1': '11417169',
    'СШІм-24-2': '11607884',
    'ДСм-24-1': '11417177',

    'ІНФм-24-1': '11416917',
    'ІНФм-24-2': '11416919',

    'ПЗПІ-21-1': '9291668',
    'ПЗПІ-21-2': '9291670',
    'ПЗПІ-21-3': '9291672',
    'ПЗПІ-21-4': '9291674',
    'ПЗПІ-21-5': '9291676',
    'ПЗПІ-21-6': '9291678',
    'ПЗПІ-21-7': '9291680',
    'ПЗПІ-21-8': '9291682',
    'ПЗПІ-21-9': '9291684',
    'ПЗПІ-21-10': '9291686',
    'ПЗПІ-21-11': '9291688',

    # 'ПЗПІ-20-1': '8476596',
    # 'ПЗПІ-20-2': '8476506',
    # 'ПЗПІ-20-3': '8476548',
    # 'ПЗПІ-20-4': '8476618',
    # 'ПЗПІ-20-5': '8744039',
    # 'ПЗПІ-20-6': '8476450',
    # 'ПЗПІ-20-7': '8476364',
    # 'ПЗПІ-20-8': '8476408',
    # 'ПЗПІ-20-9': '8476572',
    # 'ПЗПІ-20-10': '8744041',
    # 'ПЗПІи-20-1': '8832021',
    #
    # 'ПЗПІ-19-1': '7706427',
    # 'ПЗПІ-19-2': '7706511',
    # 'ПЗПІ-19-3': '7706429',
    # 'ПЗПІ-19-4': '7985998',
    # 'ПЗПІ-19-5': '7985986',
    # 'ПЗПІ-19-6': '7706393',
    # 'ПЗПІ-19-7': '7706507',
    # 'ПЗПІ-19-8': '7706315',
    # 'ПЗПІ-19-9': '7706363',
    # 'ПЗПІ-19-10': '7985982',
    # 'ПЗПІ-19-11': '7985980',
    # 'ПЗПІи-19-1': '7999876',

    # 'ПЗПІ-18-1': '6949772',
    # 'ПЗПІ-18-2': '6949830',
    # 'ПЗПІ-18-3': '6949706',
    # 'ПЗПІ-18-4': '6949774',
    # 'ПЗПІ-18-5': '7195531',
    # 'ПЗПІ-18-6': '6949688',
    # 'ПЗПІ-18-7': '6949724',
    # 'ПЗПІ-18-8': '6949726',
    # 'ПЗПІ-18-9': '6949654',
    # 'ПЗПІ-18-10': '7195529',
    # 'ПЗПІ-18-11': '7195533',
    # 'ПЗПІи-18-1': '7240401',
}

icons = {  # should be set in `local_conf.py`
    'ПЗПІ-20-4': None,
}

channels = {  # should be set in `local_conf.py`
    'ПЗПІ-19-3': None,
}

forums = {
    'ПЗПІ-23': None,
}

threads = {
    'ПЗПІ-23': None,
}

# Paths:
root_path = Path(__file__).resolve().parent
data_path = root_path / 'data'

try:
    from local_conf import *
except ImportError:
    pass
