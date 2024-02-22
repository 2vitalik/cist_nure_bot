import re

import conf
from src.data.const import times
from src.data.load import load_subjects, load_groups
from src.utils.tg import tg_send


def get_subject_links(subject):
    subjects = load_subjects()
    if subject not in subjects:
        return None, None
    return subjects[subject][1], subjects[subject][2]


def make_link(href):
    if not href or href == '?':
        return ''

    if re.fullmatch(r'https://dl\.nure\.ua/course/view\.php\?id=(\d+)', href):
        title = f'dl(c)'
    elif re.fullmatch(r'https://dl\.nure\.ua/mod/url/view\.php\?id=(\d+)', href):
        title = f'dl(u)'
    elif re.fullmatch(r'https://dl\.nure\.ua/mod/attendance/view\.php\?id=(\d+)', href):
        title = f'dl(a)'
    elif re.fullmatch(r'https://classroom\.google\.com/.*', href):
        title = f'classroom'
    elif re.fullmatch(r'https://t\.me/.*', href):
        title = f'telegram'
    elif re.fullmatch(r'https://meet\.google\.com/.*', href):
        title = f'meet'
    else:
        title = 'link'

    link = f'<a href="{href}">{title}</a>'
    # if title == 'meet':
    #     link = f'<b>{link}</b>'
    return link


def get_icon(group, kind):
    icons = {
        'лк': '💬',
        'пз': '📖',
        'лб': '⚙️',
        'ку': '🔗',
        'кс': '❓',
        'зал': '💢',
        'ісп': '💢',
        'екз': '💢',
        '!!!': '‼️',
        # todo: other types...
    }

    custom_icons = conf.icons.get(group, {})
    icons.update(custom_icons)

    return icons.get(kind, '❔')


def get_links(group, subject, kind, room, sep):
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

    if meet_links:
        # print()
        # print(f'[{subject}] ({kind}) - {group}')  # fixme: debug

        for line in meet_links.split('\n'):
            m = re.fullmatch(r'\[(.*)]: (https://meet.google.com/\w{3}-\w{4}-\w{3})', line)
            if not m:
                msg = f'Never should happen: {line}\n ' \
                      f'[{subject}] ({kind}) - {group}'
                tg_send(conf.telegram_admin, msg)
                continue

            def check_pz_lb(kind):
                raw_nums = cfg.split(',')
                nums = []
                for num in raw_nums:
                    if num == kind:
                        continue
                    elif re.fullmatch(r'\d+', num):
                        nums.append(num)
                    else:
                        m = re.fullmatch(r'(\d+)-(\d+)', num)
                        if m:
                            a, b = m.groups()
                            nums.extend(map(str, range(int(a), int(b) + 1)))
                        else:
                            msg = f'Wrong value in cfg ("{cfg}"): {line}\n ' \
                                  f'[{subject}] ({kind}) - {group}'
                            tg_send(conf.telegram_admin, msg)
                            continue

                curr_num = group[len('ПЗПІ-XX-'):]
                return curr_num in nums

            cfg, href = m.groups()
            eng = conf.group_eng[group]

            if '?' in cfg:
                ok = False
            elif kind == 'лк':
                if cfg in ['*', 'лк']:
                    ok = True
                elif cfg == 'лк-А':
                    ok = eng
                elif cfg == 'лк-У':
                    ok = not eng
                else:
                    ok = False
            elif kind in ['пз', 'лб']:
                other_kind = {'пз': 'лб', 'лб': 'пз'}[kind]
                if cfg in ['*', kind, 'пз,лб', 'лб,пз']:
                    ok = True
                elif cfg in ['лк', 'лк-А', 'лк-У']:
                    ok = False
                elif kind not in cfg and other_kind in cfg:
                    ok = False
                else:
                    ok = check_pz_lb(kind)
            else:
                ok = False

            if ok:
                # print(f'{cfg} -> {meet_link}')  # fixme: debug
                link = make_link(href)
                links.append(link)
            # else:
            #     print(f'{cfg} -> -')

    if links:
        links_text = ", ".join(links)
        return f'{sep}{links_text}'
    else:
        # return f'{sep}{room}' if room else ''
        return ''


def prettify_lesson(group, subject, kind, room, comment, sep=' → '):
    icon = get_icon(group, kind)
    links = get_links(group, subject, kind, room, sep)
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
        message += f'{alarm_icon}▫️ <code>     </code>: {line}\n'
    return message


if __name__ == '__main__':  # just for test...
    groups = load_groups()
    subjects = load_subjects()

    for subject, data in subjects.items():
        if data[2]:
            print(subject, '-' * 40)
            print(data[2])
    print('=' * 60)

    for subject in subjects:
        for kind in ['лк', 'пз', 'лб']:
            for group in groups:
                get_links(group, subject, kind, '', '')
