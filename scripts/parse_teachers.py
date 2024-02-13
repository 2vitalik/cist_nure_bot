import re
from collections import defaultdict

from scripts.data.pi_2023_s2 import pi23, pi22, pi21, pi20, pim22


def parse(input_data, max_eng, max_ukr=None):
    print('=' * 110)
    all_eng = ','.join(map(str, range(1, max_eng+1)))
    if max_ukr:
        all_ukr = ','.join(map(str, range(max_eng+1, max_ukr+1)))
    else:
        all_ukr = None

    for line in input_data.strip().split('\n'):
        m = re.fullmatch(r'([^\t]+)\t(.+) : (.*)', line)
        if not m:
            print(line)
            raise Exception()

        short, long, other = m.groups()
        if short in ['ФВ', 'ІМ']:
            continue  # skip because no teachers there

        print('-' * 100)
        print(short, '-', long)
        print('-' * 100)

        grouped_teachers = defaultdict(lambda: defaultdict(list))

        for item in other.split(':'):
            item = item.strip()
            if not item:
                continue
            m = re.fullmatch(r'(Лк|Пз|Лб) \(\d+\) - (.+?), (.*)', item)
            if not m:
                print(line)
                print(item)
                raise Exception()
            kind, groups, teachers = m.groups()
            # print(groups)
            # if not short.startswith('*'):
            #     continue
            if short.startswith('*') and '*' in groups and '(' in groups:
                groups = ['0']
                # continue  # temp
            else:
                groups = re.sub('ПЗПІ-2\d-', '', groups)
                groups = re.sub('ІПЗм-2\d-', '', groups)
                groups = re.split('[,;]', groups)
                # m = re.fullmatch(r'[\d,;]+', groups)
                # if not m:
                #     print(item)
            teachers = re.sub(' [А-ЯІЄ0]\. [А-ЯІЄ0]\.', '', teachers)
            teachers = ', '.join(set(teachers.split(', ')))
            # if len(teachers) > 1:
            # print(kind, groups, teachers)

            grouped_teachers[teachers][kind].extend(groups)

        # pprint(grouped_teachers)

        teachers_data = defaultdict(dict)
        for teacher, data in grouped_teachers.items():
            for kind, groups in data.items():
                groups = ','.join(map(str, sorted(map(int, set(groups)))))
                if groups == all_ukr:
                    groups = 'ukr'
                else:
                    if all_ukr:
                        if groups == all_eng:
                            groups = 'eng'
                        elif groups == f'{all_eng},{all_ukr}':
                            groups = 'all'
                    else:
                        if groups == all_eng:
                            groups = 'all'
                teachers_data[teacher][kind] = groups

        # pprint(teachers_data)

        for teacher, data in teachers_data.items():
            if 'Лб' in data:
                if data.get('Лб') == data.get('Пз'):
                    value = data['Лб']
                    del data['Лб']
                    del data['Пз']
                    data['Пз-Лб'] = value

        # pprint(teachers_data)
        for teacher, data in teachers_data.items():
            values = ', '.join([
                f"{kind}-{groups}".lower()
                for kind, groups in data.items()
            ])
            print(f'{teacher}: {values}')


if __name__ == '__main__':
    parse(pi23, 5, 10)
    parse(pi22, 5, 10)
    parse(pi21, 5, 11)
    parse(pi20, 5, 10)
    parse(pim22, 6)
