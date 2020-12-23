from datetime import datetime

from src.coda.get import get_subjects_from_coda, get_groups_from_coda, \
    get_records_from_coda
from src.coda.vars import coda_records, coda_subjects, coda_groups
from src.data.const import kinds
from src.utils.slack import slack_status, slack_error


def update_coda(potok_slug, new_records, new_groups, new_subjects):
    old_subjects = get_subjects_from_coda()
    old_groups = get_groups_from_coda()
    old_records = get_records_from_coda(potok_slug, no_comment=True)

    for subject in new_subjects:
        if subject not in old_subjects:
            slack_status(f'Adding subject to coda: "{subject}"')
            coda_subjects.append({'Сокращение': subject,
                                  'potok_slug': potok_slug})

    for group in new_groups:
        if group not in old_groups:
            slack_status(f'Adding group to coda: "{group}"')
            spec, year, num = group.split('-')
            coda_groups.append({'Спец': spec, "Год": year, "Номер": num,
                                'potok_slug': potok_slug})

    # todo: also process removals of groups and subjects? (mark as removed)

    # todo: make some refactoring below
    for group in sorted(new_records):
        print('=' * 100)
        print(group)
        for date_from in sorted(new_records[group]):
            print('-' * 100)
            print(date_from)
            date_coda = \
                datetime.strptime(date_from, "%d.%m.%Y").strftime("%Y/%m/%d")
            for time_from in sorted(new_records[group][date_from]):
                print('-', time_from)
                rows = new_records[group][date_from][time_from]
                for subject, kind, room in rows:
                    print(' ', subject, kind, room)

                    new_kind = kinds.get(kind, kind)
                    if kind == new_kind:
                        slack_error(f'Unknown kind: {kind}')

                    new_record = \
                        (group, date_coda, time_from, subject, new_kind, room)
                    if new_record in old_records:
                        old_records.remove(new_record)
                        continue
                    slack_status(f'Adding record to coda:\n'
                                 f'• {group}\n'
                                 f'• {date_coda} {time_from}\n'
                                 f'• {subject}, {new_kind}, {room}')
                    # todo: send also to telegram group channel
                    coda_records.append({
                        "Группа": group,
                        "Дата": date_coda,
                        "Время": time_from,
                        "Предмет": subject,
                        "Вид": new_kind,
                        "Ауд": room,
                        "potok_slug": potok_slug,
                        "sys": True,
                    })
        #             break
        #         break
        #     break
        # break
