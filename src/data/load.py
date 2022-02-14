from collections import defaultdict
from pprint import pprint

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


def load_subjects():
    subjects_entries = \
        json_load(f'{conf.data_path}/coda/json/all_subjects.json')
    subjects = {}
    for key, potok_slug, link in subjects_entries:
        if key in subjects:
            (old_potok_slug, old_link) = subjects[key]
            potok_slug += f', {old_potok_slug}'
        subjects[key] = (potok_slug, link)
    return subjects


if __name__ == '__main__':
    pprint(load_subjects())
