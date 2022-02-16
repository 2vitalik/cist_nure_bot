import re

import conf
from src.data.const import times
from src.data.load import load_subjects


def get_subject_links(subject):
    subjects = load_subjects()
    if subject not in subjects:
        return
    return subjects[subject][1]


def make_link(link):
    m_dl = re.fullmatch(r'https://dl\.nure\.ua/course/view\.php\?id=(\d+)',
                        link)
    m_classroom = re.fullmatch(r'https://classroom\.google\.com/.*', link)
    if m_dl:
        # course_id = m.group(1)
        # title = f'dl:{course_id}'
        title = f'dl.nure'
    elif m_classroom:
        title = f'classroom'
    else:
        title = 'link'
    return f'<a href="{link}">{title}</a>'


def prettify_lesson(group, subject, kind, room, comment, sep=' → '):
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

    subject_links = get_subject_links(subject)
    if subject_links:
        if '\n' in subject_links:
            two_links = subject_links.split('\n')
            if conf.group_eng[group]:
                subject_link = two_links[0]
            else:
                subject_link = two_links[1]
        else:
            subject_link = subject_links
        prettify_link = make_link(subject_link)
        room_suffix = f'{sep}{prettify_link}'
    else:
        room_suffix = f'{sep}{room}' if room else ''

    comment_line = f'\n✍️ {comment}' if comment else ''

    return f'{icon} ({kind}) <b>{subject}</b>{room_suffix}{comment_line}'


def prettify_time_slot(day_table, group, time_key, alarm=False):
    lessons = day_table[time_key][::-1]
    number = times.get(time_key, '*️⃣')
    line = prettify_lesson(group, *lessons[0][1:])
    alarm_icon = '⏰ ' if alarm else ''
    message = f'{alarm_icon}{number} <code>{time_key[:5]}</code>: {line}\n'
    for lesson in lessons[1:]:
        line = prettify_lesson(group, *lesson[1:])
        message += f'{alarm_icon}▫️<code>     </code>   {line}\n'
    return message
