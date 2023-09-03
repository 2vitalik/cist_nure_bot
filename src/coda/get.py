from src.coda.lib import dt_text
from src.coda.vars import coda_subjects, coda_groups, coda_records


def get_subjects_from_coda():
    subjects = list()
    entries = coda_subjects.rows_dict()
    for entry in entries.values():
        subjects.append((entry['Сокращение'], entry['potok_slug'],
                         entry['link'], entry['Meet-посилання']))
    return sorted(subjects)


def get_groups_from_coda():
    groups = list()
    entries = coda_groups.rows_dict()
    for entry in entries.values():
        groups.append((entry['Группа'], entry['potok_slug']))
    return sorted(groups)


def get_records_from_coda(cist_comparable=False):
    records = list()
    entries = coda_records.rows_dict()
    for coda_id, entry in entries.items():
        if cist_comparable:
            if entry['removed'] or not entry['sys']:
                continue
        else:
            if entry['removed'] or not entry['visible']:
                continue
        value = (
            coda_id,
            entry['Группа'], dt_text(entry['Дата']), dt_text(entry['Время']),
            entry['Предмет'], entry['Вид'], entry['Ауд'], entry['Комментарий'],
            entry['potok_slug'],
        )
        records.append(value)
    return sorted(records)
