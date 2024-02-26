import json
from collections import defaultdict

from src.data.load import load_potok_groups, load_potok_subjects
from src.msgs.prettify import LinksProcessor


def join_equal_kinds(subject_data):
    if not subject_data:
        return
    if subject_data['пз'] == subject_data['лб']:
        subject_data['пз,лб'] = subject_data['пз']
        subject_data.pop('пз')
        subject_data.pop('лб')
        if subject_data.get('лк') == subject_data['пз,лб']:
            subject_data['*'] = subject_data['лк']
            subject_data.pop('лк')
            subject_data.pop('пз,лб')


def convert_ranges(groups):
    i = 0
    while i < len(groups) - 1:
        j = i + 1
        while j < len(groups) and groups[j] - groups[j-1] == 1:
            j += 1
        if j != i + 1:
            groups[i] = f'{groups[i]}-{groups[j-1]}'
            del groups[i+1:j]
        i += 1


def shorten_group_list(groups):
    groups = [int(group[3:]) for group in groups]
    convert_ranges(groups)
    return ', '.join(map(str, groups))


def dict_potok_subject_kind_groups_links():
    result = {}
    groups = load_potok_groups()
    subjects = load_potok_subjects()
    for potok_slug, data in subjects.items():
        result[potok_slug] = {}
        for subject, (link, meet) in data.items():
            result[potok_slug][subject] = defaultdict(dict)
            subject_data = defaultdict(dict)
            for kind in ['лк', 'пз', 'лб']:
                links_data = defaultdict(list)
                for group in groups[potok_slug]:
                    links = LinksProcessor(group, subject, kind, '', '').links
                    if links:
                        links_key = ', '.join(links)
                        links_data[links_key].append(group[len('ПЗПІ-'):])
                if links_data:
                    for links_key, groups_list in links_data.items():
                        groups_key = shorten_group_list(groups_list)
                        subject_data[kind][groups_key] = links_key
            join_equal_kinds(subject_data)
            result[potok_slug][subject] = subject_data

    return result


if __name__ == '__main__':
    print(json.dumps(dict_potok_subject_kind_groups_links(),
                     ensure_ascii=False, indent=4))
