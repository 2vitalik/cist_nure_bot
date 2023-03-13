import conf
from src.coda.get import get_subjects_from_coda, get_groups_from_coda, \
    get_records_from_coda
from src.utils.dump import dump_json_data


def dump_coda():
    subjects = get_subjects_from_coda()
    groups = get_groups_from_coda()
    records = get_records_from_coda()

    path = f'{conf.data_path}/coda'
    dump_json_data(path, 'all', kind='coda',
                   names=[
                       'subjects',
                       'groups',
                       'records',
                   ],
                   values=[
                       subjects,
                       groups,
                       records,
                   ])
