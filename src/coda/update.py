import time
from datetime import datetime, timedelta
from urllib.error import HTTPError

import conf
from src.cist.parse import load_cist_parsed
from src.coda.get import get_subjects_from_coda, get_groups_from_coda, \
    get_records_from_coda
from src.coda.vars import coda_records, coda_subjects, coda_groups
from src.data.const import kinds, times
from src.data.load import group_records
from src.msgs.prettify import prettify_lesson
from src.utils.date import prettify_date
from src.utils.slack import slack_status, slack_error
from src.utils.tg import tg_send


def group_slot(rows, source):
    slot = {}
    for row in rows:
        if source == 'cist':
            subject, kind, room = row
            new_kind = kinds.get(kind, kind)
            if new_kind == kind:
                # never should happen
                slack_error(f'🚫 Unknown kind: "{kind}"')
                time.sleep(0.5)
            coda_id = '?'
            kind = new_kind
        elif source == 'coda':
            coda_id, subject, kind, room, comment = row
        else:
            raise Exception('Never should happen in `group_slot`')

        key = (subject, kind)
        if key in slot:
            # never should happen
            # slack_error(f'🚫 Several rooms for the slot: "{key}"')
            pass  # fixme !!!

        slot[key] = (coda_id, room)
    return slot


def prettify_line(group, time_key, subject, kind, room, comment=''):
    number = times.get(time_key, '*️⃣')
    line = prettify_lesson(group, subject, kind, room, comment, sep='  ')
    message = f'{number} <code>{time_key[:5]}</code>: {line}'
    return message


def update_coda():
    all_old_subjects = get_subjects_from_coda()
    all_old_groups = get_groups_from_coda()
    all_old_records = get_records_from_coda(cist_comparable=True)

    # fixme: this is just for faster debugging...
    # from shared_utils.io.json import json_load
    # all_old_records = \
    #     json_load(f'{conf.data_path}/coda/json/all_records.json')

    for potok_slug in conf.groups:
        old_subjects = [subject
                        for subject, old_potok_slug, _, _ in all_old_subjects
                        if potok_slug in old_potok_slug]
        old_groups = [group
                      for group, old_potok_slug in all_old_groups
                      if old_potok_slug == potok_slug]
        old_records = [(*values, old_potok_slug)
                       for *values, old_potok_slug in all_old_records
                       if old_potok_slug == potok_slug]
        old_records = group_records(old_records)

        new_records, new_groups, new_subjects = load_cist_parsed(potok_slug)

        for subject in new_subjects:
            if subject not in old_subjects:
                slack_status(f'➕ `{potok_slug}`  new subject: *"{subject}"*')
                coda_subjects.append({'Сокращение': subject,
                                      'potok_slug': potok_slug})
                time.sleep(0.5)
        removed_subjects = set(old_subjects) - set(new_subjects)
        for subject in removed_subjects:
            slack_error(f'❌ `{potok_slug}`  removed subject: *"{subject}"*')
            time.sleep(0.5)
            # todo: mark as "removed" in coda?

        for group in new_groups:
            if group not in old_groups:
                slack_status(f'➕ `{potok_slug}`  new group: "{group}"')
                spec, year, num = group.split('-')
                coda_groups.append({'Спец': spec, "Год": year, "Номер": num,
                                    'potok_slug': potok_slug})
                time.sleep(0.5)
        removed_groups = set(old_groups) - set(new_groups)
        for subject in removed_groups:
            slack_error(f'❌ `{potok_slug}`  removed group: *"{subject}"*')
            time.sleep(0.5)
            # todo: mark as "removed" in coda?

        max_changes_date = datetime.now() + timedelta(10)
        min_changes_date = datetime.now() - timedelta(1)

        for group in sorted(old_records):
            # print('=' * 100)
            # print(group)

            # fixme: debug only:
            if group not in conf.channels:
                print(f'group "{group}" not in `conf.channels`')
                continue

            channel_id = conf.channels[group]

            for date_coda in sorted(old_records[group]):
                # print('-' * 100)
                # print(date_from)
                day = datetime.strptime(date_coda[:10], "%Y/%m/%d")
                date_from = day.strftime("%Y-%m-%d")
                day_prettify = prettify_date(day)
                header = f'⚠️ Зміна в розкладі\n\n' \
                         f'▪️ {day_prettify}'
                changes = ''

                for time_from in sorted(old_records[group][date_coda]):
                    # print('-', time_from)

                    old_rows = old_records[group][date_coda][time_from]
                    new_rows = new_records.get(group, {}).get(date_from, {}).\
                        get(time_from, [])

                    old_slot = group_slot(old_rows, 'coda')
                    new_slot = group_slot(new_rows, 'cist')

                    for (subject, kind) in old_slot:
                        if (subject, kind) not in new_slot:
                            coda_id, room = old_slot[(subject, kind)]
                            slack_status(f'❌ `{potok_slug}`  remove lesson: '
                                         f'*{group} '
                                         f' 📆 {date_from} '
                                         f' ⏱ {time_from} '
                                         f' 📝 {subject}, {kind}, {room}*')
                            coda_records.update(coda_id, {"removed": True})
                            if min_changes_date <= day <= max_changes_date:
                                line = prettify_line(group, time_from,
                                                     subject, kind, room)
                                changes += f'❌ {line}\n'
                            time.sleep(0.5)

                if changes and not conf.temporary_disable_tg:
                    tg_send(channel_id, f'{header}\n{changes}')
                    slack_status('⚠️ _Sent to telegram-channel_')

        for group in sorted(new_records):
            # print('=' * 100)
            # print(group)

            # fixme: debug only:
            if group not in conf.channels:
                print(f'group "{group}" not in `conf.channels`')
                continue

            channel_id = conf.channels[group]

            for date_from in sorted(new_records[group]):
                # print('-' * 100)
                # print(date_from)
                day = datetime.strptime(date_from[:10], "%Y-%m-%d")
                date_coda = day.strftime("%Y/%m/%d")
                day_prettify = prettify_date(day)
                header = f'⚠️ Зміна в розкладі\n\n' \
                         f'▪️ {day_prettify}'
                changes = ''

                for time_from in sorted(new_records[group][date_from]):
                    # print('-', time_from)

                    old_rows = old_records[group][date_coda][time_from]
                    new_rows = new_records[group][date_from][time_from]

                    old_slot = group_slot(old_rows, 'coda')
                    new_slot = group_slot(new_rows, 'cist')

                    for (subject, kind) in old_slot:
                        if (subject, kind) not in new_slot:
                            coda_id, room = old_slot[(subject, kind)]
                            slack_status(f'❌ `{potok_slug}`  remove lesson: '
                                         f'*{group} '
                                         f' 📆 {date_from} '
                                         f' ⏱ {time_from} '
                                         f' 📝 {subject}, {kind}, {room}*')
                            coda_records.update(coda_id, {"removed": True})
                            if min_changes_date <= day <= max_changes_date:
                                line = prettify_line(group, time_from,
                                                     subject, kind, room)
                                changes += f'❌ {line}\n'
                            time.sleep(0.5)

                    for (subject, kind) in new_slot:
                        if (subject, kind) not in old_slot:
                            coda_id, room = new_slot[(subject, kind)]
                            if not conf.temporary_disable_slack_new:
                                slack_status(f'➕ `{potok_slug}`  new lesson: '
                                             f'*{group} '
                                             f' 📆 {date_from} '
                                             f' ⏱ {time_from} '
                                             f' 📝 {subject}, {kind}, {room}*')
                            coda_records.append({
                                "Группа": group,
                                "Дата": date_coda,
                                "Время": time_from,
                                "Предмет": subject,
                                "Вид": kind,
                                "Ауд": room,
                                "potok_slug": potok_slug,
                                "sys": True,
                            })
                            if day < datetime.now() + timedelta(8):
                                line = prettify_line(group, time_from,
                                                     subject, kind, room)
                                changes += f'➕ {line}\n'
                            time.sleep(1)

                    for (subject, kind) in old_slot:
                        if (subject, kind) in new_slot:
                            coda_id, old_room = old_slot[(subject, kind)]
                            _______, new_room = new_slot[(subject, kind)]
                            if old_room != new_room:
                                slack_status(
                                    f'🌀 `{potok_slug}`  change lesson: '
                                    f'*{group} '
                                    f' 📆 {date_from}  ⏱ {time_from} '
                                    f' 📝 {subject}, {kind}, '
                                    f' "{old_room}" → "{new_room}"*')
                                try:
                                    coda_records.update(coda_id,
                                                        {"Ауд": new_room})
                                except HTTPError:
                                    slack_error('`coda`: HTTPError')
                                    # todo: one more attempt?
                                    raise
                                if min_changes_date <= day <= max_changes_date \
                                        and False:  # make sense only "offline"
                                    line = prettify_line(group, time_from,
                                                         subject, kind,
                                                         old_room)
                                    changes += f'🌀 {line} → {new_room}\n'
                                time.sleep(0.5)

                if changes and not conf.temporary_disable_tg:
                    tg_send(channel_id, f'{header}\n{changes}')
                    slack_status('⚠️ _Sent to telegram-channel_')
