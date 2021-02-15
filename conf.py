
coda_token = None  # should be set in `local_conf.py`
telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

date_from = '01.02.2021'
date_to = '30.07.2021'

groups = {
    'pzpi-20': '8476596_8476506_8476548_8476618_8744039_8476450_8476364_'
               '8476408_8476572_8744041_8832021',
    'pzpi-19': '7706427_7999876_7706511_7706429_7985986_7985998_7706363_'
               '7706315_7706393_7985980_7985982_7706507',
    'pzpi-18': '6949772_7240401_6949830_6949706_6949774_7195531_6949688_'
               '6949724_6949726_6949654_7195529_7195533',
    'pzpi-17': '6283365_6283375_6496576_6496579_6283463_6283489_6283409_'
               '6496585_6496598_7197629_6569333',
}

channels = {  # should be set in `local_conf.py`
    'ПЗПІ-19-3': None,
}

data_path = 'data'

try:
    from local_conf import *
except ImportError:
    pass
