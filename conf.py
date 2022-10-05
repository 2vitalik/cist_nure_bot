
coda_token = None  # should be set in `local_conf.py`
telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

semester = '2022-2'
date_from = '01.09.2022'
date_to = '01.02.2023'

temporary_disable_tg = False
temporary_disable_slack_new = False

groups = {
    'pzpi-22': '10284307_10284309_10284313_10284311_10537885_10284315_'
               '10284317_10284319_10284321_10537887',
    'ipzm-22': '10284301_10284303_10539519_10539521_10539523_10539525_10539534',
    'pzpi-21': '9291668_9291670_9291672_9291674_9291676_9291678_9291680_'
               '9291682_9291684_9291686_9291688',
    'pzpi-20': '8476596_8476506_8476548_8476618_8744039_8476450_8476364_'
               '8476408_8476572_8744041_8832021',
    'pzpi-19': '7706427_7999876_7706511_7706429_7985986_7985998_7706363_'
               '7706315_7706393_7985980_7985982_7706507',
    # 'pzpi-18': '6949772_7240401_6949830_6949706_6949774_7195531_6949688_'
    #            '6949724_6949726_6949654_7195529_7195533',
    # 'pzpi-17': '6283365_6283375_6496576_6496579_6283463_6283489_6283409_'
    #            '6496585_6496598_7197629_6569333',
}

group_eng = {
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

    'ІПЗм-22-1': True,
    'ІПЗм-22-2': True,
    'ІПЗм-22-3': True,
    'ІПЗм-22-4': True,
    'ІПЗм-22-5': True,
    'ІПЗм-22-6': True,
    'ІПЗм-22-7': True,

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

    'ПЗПІ-20-1': True,
    'ПЗПІ-20-2': True,
    'ПЗПІ-20-3': True,
    'ПЗПІ-20-4': True,
    'ПЗПІ-20-5': True,
    'ПЗПІ-20-6': False,
    'ПЗПІ-20-7': False,
    'ПЗПІ-20-8': False,
    'ПЗПІ-20-9': False,
    'ПЗПІ-20-10': False,
    'ПЗПІи-20-1': False,

    'ПЗПІ-19-1': True,
    'ПЗПІ-19-2': True,
    'ПЗПІ-19-3': True,
    'ПЗПІ-19-4': True,
    'ПЗПІ-19-5': True,
    'ПЗПІ-19-6': False,
    'ПЗПІ-19-7': False,
    'ПЗПІ-19-8': False,
    'ПЗПІ-19-9': False,
    'ПЗПІ-19-10': False,
    'ПЗПІ-19-11': False,
    'ПЗПІи-19-1': False,

    'ПЗПІ-18-1': True,
    'ПЗПІ-18-2': True,
    'ПЗПІ-18-3': True,
    'ПЗПІ-18-4': True,
    'ПЗПІ-18-5': True,
    'ПЗПІ-18-6': False,
    'ПЗПІ-18-7': False,
    'ПЗПІ-18-8': False,
    'ПЗПІ-18-9': False,
    'ПЗПІ-18-10': False,
    'ПЗПІ-18-11': False,
    'ПЗПІи-18-1': False,
}

cist_ids = {
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

    'ІПЗм-22-1': '10284301',
    'ІПЗм-22-2': '10284303',
    'ІПЗм-22-3': '10539519',
    'ІПЗм-22-4': '10539521',
    'ІПЗм-22-5': '10539523',
    'ІПЗм-22-6': '10539525',
    'ІПЗм-22-7': '10539534',

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

    'ПЗПІ-20-1': '8476596',
    'ПЗПІ-20-2': '8476506',
    'ПЗПІ-20-3': '8476548',
    'ПЗПІ-20-4': '8476618',
    'ПЗПІ-20-5': '8744039',
    'ПЗПІ-20-6': '8476450',
    'ПЗПІ-20-7': '8476364',
    'ПЗПІ-20-8': '8476408',
    'ПЗПІ-20-9': '8476572',
    'ПЗПІ-20-10': '8744041',
    'ПЗПІи-20-1': '8832021',

    'ПЗПІ-19-1': '7706427',
    'ПЗПІ-19-2': '7706511',
    'ПЗПІ-19-3': '7706429',
    'ПЗПІ-19-4': '7985998',
    'ПЗПІ-19-5': '7985986',
    'ПЗПІ-19-6': '7706393',
    'ПЗПІ-19-7': '7706507',
    'ПЗПІ-19-8': '7706315',
    'ПЗПІ-19-9': '7706363',
    'ПЗПІ-19-10': '7985982',
    'ПЗПІ-19-11': '7985980',
    'ПЗПІи-19-1': '7999876',

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

channels = {  # should be set in `local_conf.py`
    'ПЗПІ-19-3': None,
}

data_path = 'data'

try:
    from local_conf import *
except ImportError:
    pass
