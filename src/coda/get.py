from src.coda.lib import dt_text
from src.coda.vars import coda_subjects, coda_groups, coda_records


def get_subjects_from_coda():
    subjects = list()
    entries = coda_subjects.rows_dict()
    for entry in entries.values():
        subjects.append(entry['Сокращение'])
    return subjects


def get_groups_from_coda():
    groups = list()
    entries = coda_groups.rows_dict()
    for entry in entries.values():
        groups.append(entry['Название'])
    return groups


def get_records_from_coda(potok_slug=None):
    records = list()
    entries = coda_records.rows_dict()
    for entry in entries.values():
        if potok_slug and potok_slug != entry['potok_slug']:
            continue
        records.append((
            entry['Группа'], dt_text(entry['Дата']), dt_text(entry['Время']),
            entry['Предмет'], entry['Вид'], entry['Ауд'], entry['Комментарий'],
        ))
    return records
