from src.coda.lib import dt_text
from src.coda.vars import coda_subjects, coda_groups, coda_records


def get_subjects_from_coda():
    subjects = list()
    entries = coda_subjects.rows_dict()
    for entry in entries.values():
        subjects.append(entry['Сокращение'])
    return sorted(subjects)


def get_groups_from_coda():
    groups = list()
    entries = coda_groups.rows_dict()
    for entry in entries.values():
        groups.append(entry['Название'])
    return sorted(groups)


def get_records_from_coda(potok_slug=None, no_comment=False):
    records = list()
    entries = coda_records.rows_dict()
    for entry in entries.values():
        if potok_slug and potok_slug != entry['potok_slug']:
            continue
        value = (
            entry['Группа'], dt_text(entry['Дата']), dt_text(entry['Время']),
            entry['Предмет'], entry['Вид'], entry['Ауд'], entry['Комментарий'],
        )
        if no_comment:
            value = value[:-1]  # without comment
        records.append(value)
    return sorted(records)
