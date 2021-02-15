import up  # to go to root folder
from datetime import datetime

from shared_utils.conf import conf as shared_conf

import conf
from src.coda.update import update_coda
from src.utils.slack import slack


@slack('cist_to_coda')
def cist_to_coda():
    update_coda()


if __name__ == '__main__':
    print(datetime.now())

    shared_conf.slack_hooks = conf.slack_hooks
    cist_to_coda()


# todo: integrate this command into `load_cist` later
