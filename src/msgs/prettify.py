import re

import conf
from src.data.const import times
from src.data.load import load_subjects


def get_subject_links(subject):
    subjects = load_subjects()
    if subject not in subjects:
        return
    return subjects[subject][1], subjects[subject][2]


def make_link(link):
    if not link or link == '?':
        return ''

    m_dl = re.fullmatch(r'https://dl\.nure\.ua/course/view\.php\?id=(\d+)',
                        link)
    m_classroom = re.fullmatch(r'https://classroom\.google\.com/.*', link)
    m_tg = re.fullmatch(r'https://t\.me/.*', link)
    if m_dl:
        title = f'dl.nure'
    elif m_classroom:
        title = f'classroom'
    elif m_tg:
        title = f'telegram'
    else:
        title = 'link'
    return f'<a href="{link}">{title}</a>'


def get_icon(group, kind):
    # todo: get related icon for student group...
    icons = {
        'лк': '📖',
        'пз': '💬',
        'лб': '⚙️',
        'ку': '🔗',
        'кс': '❓',
        'зал': '💢',
        'ісп': '💢',
        'екз': '💢',
        '!!!': '‼️',
        # todo: other types...
    }
    return icons.get(kind, '❔')


def get_links(group, subject, room, sep):
    dl_links, meet_links = get_subject_links(subject)

    links = []
    if dl_links:
        if '\n' in dl_links:
            two_links = dl_links.split('\n')
            if conf.group_eng[group]:
                href = two_links[0]
            else:
                href = two_links[1]
        else:
            href = dl_links
        link = make_link(href)
        links.append(link)

    if links:
        links_text = ", ".join(links)
        return f'{sep}{links_text}'
    else:
        return f'{sep}{room}' if room else ''


def prettify_lesson(group, subject, kind, room, comment, sep=' → '):
    icon = get_icon(group, kind)
    links = get_links(group, subject, room, sep)
    comment_line = f'\n✍️ {comment}' if comment else ''

    return f'{icon} ({kind}) <b>{subject}</b>{links}{comment_line}'


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
