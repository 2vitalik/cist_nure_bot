from collections import defaultdict

from shared_utils.io.json import json_load

import conf


def load_data():
    path = f'{conf.data_path}/coda'
    records_entries = json_load(f'{path}/all_records.json')

    records = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in records_entries:
        group, date_from, time_from, subject, kind, room = entry
        records[group][date_from][time_from].append((subject, kind, room))

    return records
