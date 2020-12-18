
coda_token = None  # should be set in `local_conf.py`
telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

try:
    from local_conf import *
except ImportError:
    pass
