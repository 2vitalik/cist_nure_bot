import re

from src.data.const import times
from src.data.load import load_subjects


def get_subject_link(subject):
    subjects = load_subjects()
    if subject not in subjects:
        return
    return subjects[subject][1]

def prettify_lesson(subject, kind, room, comment, sep=' → '):
    icons = {
        'лк': '📖',
        'пз': '💬',
        'лб': '⚙️',
        'кс': '❓',
        'зал': '💢',
        'ісп': '💢',
        'екз': '💢',
        '!!!': '‼️',
    }
    icon = icons.get(kind, '❔')
    subject_link = get_subject_link(subject)
    if subject_link:
        m = re.fullmatch(r'https://dl\.nure\.ua/course/view\.php\?id=(\d+)',
                         subject_link)
        if m:
            # course_id = m.group(1)
            # title = f'dl:{course_id}'
            title = f'dl.nure'
        else:
            title = 'link'
        room_suffix = f'{sep}<a href="{subject_link}">{title}</a>'
    else:
        room_suffix = f'{sep}{room}' if room else ''
    comment_line = f'\n✍️ {comment}' if comment else ''
    return f'{icon} ({kind}) <b>{subject}</b>{room_suffix}{comment_line}'


def prettify_time_slot(day_table, time_key, alarm=False):
    lessons = day_table[time_key][::-1]
    number = times.get(time_key, '*️⃣')
    line = prettify_lesson(*lessons[0][1:])
    alarm_icon = '⏰ ' if alarm else ''
    message = f'{alarm_icon}{number} <code>{time_key[:5]}</code>: {line}\n'
    for lesson in lessons[1:]:
        line = prettify_lesson(*lesson[1:])
        message += f'{alarm_icon}▫️<code>     </code>   {line}\n'
    return message
