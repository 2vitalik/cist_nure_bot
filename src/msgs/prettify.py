import json
import re
from collections import defaultdict

import conf
from src.data.const import times
from src.data.load import load_subjects, load_potok_subjects, load_potok_groups
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
    elif re.fullmatch(r'https://nure-ua\.zoom\.us/.*', href):
        title = f'zoom'
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


class LinksProcessor:

    def __init__(self, group, subject, kind, room, sep):
        self.group = group
        self.subject = subject
        self.kind = kind
        self.room = room
        self.sep = sep

        dl_links, meet_links = get_subject_links(subject)
        self.links = self.process_links(dl_links, meet_links)

    def process_links(self, dl_links, meet_links):
        links = []
        if dl_links:
            if '\n' in dl_links:
                two_links = dl_links.split('\n')
                if conf.group_eng[self.group]:
                    href = two_links[0]
                else:
                    href = two_links[1]
            else:
                href = dl_links
            links.append(href)

        if meet_links:
            # print()
            # print(f'[{subject}] ({kind}) - {group}')  # fixme: debug

            for line in meet_links.split('\n'):
                m = re.fullmatch(r'\[(.*)]: (https://.*)', line)  # fixme: meet.google.com/\w{3}-\w{4}-\w{3}
                if not m:
                    msg = f'Wrong meet-filter line: {line}\n ' \
                          f'[{self.subject}] ({self.kind}) - {self.group}'
                    tg_send(conf.telegram_admin, msg)
                    continue

                cfg, href = m.groups()

                if self.check_filter(cfg, line):
                    # print(f'{cfg} -> {meet_link}')  # fixme: debug
                    links.append(href)
                # else:
                #     print(f'{cfg} -> -')

        return links

    def check_pz_lb(self, cfg, line):
        max_eng, max_ukr = conf.group_nums[self.group[:len('ПЗПІ-XX')]].values()

        raw_nums = cfg.split(',')
        nums = []
        for num in raw_nums:
            if num == self.kind:
                continue
            elif re.fullmatch(r'\d+', num):
                nums.append(num)
            elif num == 'А':
                nums.extend(map(str, range(1, max_eng + 1)))
            elif num == 'У':
                nums.extend(map(str, range(max_eng, max_ukr + 1)))
            else:
                m = re.fullmatch(r'(\d+)-(\d+)', num)
                if m:
                    a, b = m.groups()
                    nums.extend(map(str, range(int(a), int(b) + 1)))
                else:
                    msg = f'Wrong value in cfg ("{cfg}"): {line}\n ' \
                          f'[{self.subject}] ({self.kind}) - {self.group}'
                    tg_send(conf.telegram_admin, msg)
                    continue

        curr_num = self.group[len('ПЗПІ-XX-'):]
        return curr_num in nums

    def check_filter(self, cfg, line):
        eng = conf.group_eng[self.group]

        if '?' in cfg:
            return False
        elif self.kind == 'лк':
            if cfg in ['*', 'лк']:
                return True
            elif cfg in ['лк-А', 'А']:
                return eng
            elif cfg in ['лк-У', 'У']:
                return not eng
            else:
                return False
        elif self.kind in ['пз', 'лб']:
            other_kind = {'пз': 'лб', 'лб': 'пз'}[self.kind]
            if cfg in ['*', self.kind, 'пз,лб', 'лб,пз']:
                return True
            elif cfg in ['лк', 'лк-А', 'лк-У']:
                return False
            elif self.kind not in cfg and other_kind in cfg:
                return False
            else:
                return self.check_pz_lb(cfg, line)
        else:
            return False


def get_links_text(links, sep=' → '):
    if links:
        links_text = ", ".join([make_link(link) for link in links])
        return f'{sep}{links_text}'
    else:
        # return f'{sep}{room}' if room else ''
        return ''


def prettify_lesson(group, subject, kind, room, comment, sep=' → '):
    icon = get_icon(group, kind)
    links = LinksProcessor(group, subject, kind, room, sep).links
    links_text = get_links_text(links, sep)
    comment_line = f'\n✍️ {comment}' if comment else ''

    return f'{icon} ({kind}) <b>{subject}</b>{links_text}{comment_line}'


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
    # subjects = load_subjects()
    # for subject, data in subjects.items():
    #     if data[2]:
    #         print(subject, '-' * 40)
    #         print(data[2])
    # print('=' * 60)

    result = {}
    groups = load_potok_groups()
    subjects = load_potok_subjects()
    for potok_slug, data in subjects.items():
        result[potok_slug] = {}
        for subject, (link, meet) in data.items():
            result[potok_slug][subject] = defaultdict(dict)
            for kind in ['лк', 'пз', 'лб']:
                links_data = defaultdict(list)
                for group in groups[potok_slug]:
                    links = LinksProcessor(group, subject, kind, '', '').links
                    if links:
                        links_key = ', '.join(links)
                        links_data[links_key].append(group[len('ПЗПІ-'):])
                if links_data:
                    for links_key, groups_list in links_data.items():
                        groups_key = ', '.join(groups_list)
                        result[potok_slug][subject][kind][groups_key] = links_key
    print(json.dumps(result, ensure_ascii=False, indent=4))
