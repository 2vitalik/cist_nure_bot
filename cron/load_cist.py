import up  # to go to root folder
from datetime import datetime

from shared_utils.conf import conf as shared_conf

import conf
from src.cist.download import download_cist
from src.cist.parse import parse_cist_csv, save_cist_parsed
from src.utils.slack import slack


@slack('load_cist')
def load_cist():
    for potok_slug, group_ids in conf.groups.items():
        ok = download_cist(group_ids, conf.date_from, conf.date_to, potok_slug)
        if not ok:
            return
        save_cist_parsed(potok_slug, *parse_cist_csv(potok_slug))


if __name__ == '__main__':
    print(datetime.now())

    shared_conf.slack_hooks = conf.slack_hooks
    load_cist()
