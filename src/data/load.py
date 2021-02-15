from collections import defaultdict

from shared_utils.io.json import json_load

import conf


def group_records(entries):
    records = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in entries:
        coda_id, group, date_from, time_from, \
            subject, kind, room, comment, potok_slug = entry
        value = (coda_id, subject, kind, room, comment)
        records[group][date_from][time_from].append(value)
    return records


def load_records():
    records_entries = json_load(f'{conf.data_path}/coda/json/all_records.json')
    return group_records(records_entries)
