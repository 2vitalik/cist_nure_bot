
coda_token = None  # should be set in `local_conf.py`
telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`


try:
    from local_conf import *
except ImportError:
    pass
