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
    for key, potok_slug, link, meet in subjects_entries:
        if key in subjects:
            (old_potok_slug, old_link, old_meet) = subjects[key]
            potok_slug += f', {old_potok_slug}'
        subjects[key] = (potok_slug, link, meet)
    return subjects


def load_groups():
    groups_entries = \
        json_load(f'{conf.data_path}/coda/json/all_groups.json')
    groups = []
    for group, potok_slug in groups_entries:
        groups.append(group)
    return groups


if __name__ == '__main__':
    pprint(load_subjects())
    pprint(load_groups())
