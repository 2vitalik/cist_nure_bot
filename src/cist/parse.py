from collections import defaultdict

from shared_utils.io.io import read
from shared_utils.io.json import json_load

import conf
from src.data.const import times
from src.utils.dump import dump_json_data


def check_unexpected_value(name, value, correct):
    if value != correct:
        raise ValueError(f"Unexpected `{name}`: '{value}' != '{correct}'")


def parse_cist_csv(potok_slug):
    path = f'{conf.data_path}/cist/csv'
    csv_filename = f'{path}/{potok_slug}.csv'

    groups = set()
    subjects = set()

    records = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    content = read(csv_filename)
    for line in content.split('\n')[1:]:
        if not line:
            continue

        cols = line[1:-1].split('","')
        title, date_from, time_from, date_to, time_to, \
            col6, col7, col8, col9, col10, col11, col12, col13 = cols

        if time_from not in times:
            raise ValueError(f"Unexpected time: {time_from}")

        check_unexpected_value('col6', col6, "Ложь")
        check_unexpected_value('col7', col7, "Истина")
        check_unexpected_value('col8', col8, date_from)
        check_unexpected_value('col10', col10, "2")
        check_unexpected_value('col11', col11, "Обычная")
        check_unexpected_value('col13', col13, "Обычный")

        day, month, year = date_from.split('.')
        date_from = f'{year}-{month}-{day}'

        group, rest = title.split(' - ')
        groups.add(group)

        check_unexpected_value('col12', col12, rest)

        # todo: fix this in a good way:
        rest = rest.replace('*БПС (', '*БПС(')
        rest = rest.replace('*ОсBI (', '*ОсBI(')
        rest = rest.replace('*ОSMM (', '*ОSMM(')
        rest = rest.replace('*А (advance)', '*А(advance)')
        rest = rest.replace('*ПМЗ (', '*ПМЗ(')

        values = rest.split(' ')
        if len(values) == 5:
            subject, kind, room, room_2, group_detailed = values
            subjects.add(subject)

            if not room.endswith(','):
                raise ValueError(f"Room should end with comma: '{room}'")
            room = room.rstrip(',')

            records[group][date_from][time_from].append(
                (subject, kind, f"{room}, {room_2}")
            )
        else:
            parts = rest.split('; ')
            for part in parts:
                subject, kind, room, group_detailed = part.split(' ')
                subjects.add(subject)

                records[group][date_from][time_from].append(
                    (subject, kind, room)
                )

    # sort all levels of records:
    sorted_records = {}
    for group in sorted(records):
        sorted_records[group] = {}
        for date_from in sorted(records[group]):
            sorted_records[group][date_from] = {}
            for time_from in sorted(records[group][date_from]):
                sorted_records[group][date_from][time_from] = \
                    sorted(records[group][date_from][time_from])

    return sorted_records, sorted(groups), sorted(subjects)


def save_cist_parsed(potok_slug, records, groups, subjects):
    path = f'{conf.data_path}/cist'

    dump_json_data(path, potok_slug, kind='cist',
                   names=['records', 'groups', 'subjects'],
                   values=[records, groups, subjects])


def load_cist_parsed(potok_slug):
    path = f'{conf.data_path}/cist/json'

    records = json_load(f'{path}/{potok_slug}_records.json')
    groups = json_load(f'{path}/{potok_slug}_groups.json')
    subjects = json_load(f'{path}/{potok_slug}_subjects.json')

    return records, groups, subjects


if __name__ == '__main__':
    parse_cist_csv('pzpi-19')
