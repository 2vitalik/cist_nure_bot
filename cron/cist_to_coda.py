import up  # to go to root folder

from shared_utils.conf import conf as shared_conf

import conf
from src.cist.parse import load_cist_parsed
from src.coda.update import update_coda
from src.utils.slack import slack


@slack('cist_to_coda')
def cist_to_coda():
    for potok_slug in conf.groups:
        update_coda(potok_slug, *load_cist_parsed(potok_slug))


if __name__ == '__main__':
    shared_conf.slack_hooks = conf.slack_hooks
    cist_to_coda()


# todo: integrate this command into `load_cist` later
