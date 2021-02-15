import up  # to go to root folder
from datetime import datetime

from shared_utils.conf import conf as shared_conf

import conf
from src.coda.dump import dump_coda
from src.utils.slack import slack


@slack('load_coda')
def load_coda():
    dump_coda()


if __name__ == '__main__':
    print(datetime.now())

    shared_conf.slack_hooks = conf.slack_hooks
    load_coda()
