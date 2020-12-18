from shared_utils.conf import conf as shared_conf

import conf
from src.cist.download import download_cist
from src.cist.parse import parse_csv, save_parsed
from src.utils.slack import slack


@slack('load_cist')
def load_cist():
    for group_slug, group_ids in conf.groups.items():
        download_cist(group_ids, conf.date_from, conf.date_to, group_slug)
        save_parsed(group_slug, *parse_csv(group_slug))


if __name__ == '__main__':
    shared_conf.slack_hooks = conf.slack_hooks
    load_cist()
