
coda_token = None  # should be set in `local_conf.py`
telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

date_from = '01.09.2020'
date_to = '31.01.2021'

groups = {
    'pzpi-19': '7706427_7999876_7706511_7706429_7985986_7985998_7706363_'
               '7706315_7706393_7985980_7985982_7706507',
}

channels = {  # should be set in `local_conf.py`
    'ПЗПІ-19-3': None,
}

data_path = 'data'

try:
    from local_conf import *
except ImportError:
    pass
