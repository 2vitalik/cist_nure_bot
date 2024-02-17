import re
from collections import defaultdict

from scripts.data.pi_2024_s1 import pi23, pi22, pi21, pi20


potoks = {
    'pi23': {
        'input_data': pi23,
        'max_eng_group': 5,
        'max_ukr_group': 10,
    },
    'pi22': {
        'input_data': pi22,
        'max_eng_group': 5,
        'max_ukr_group': 10,
    },
    'pi21': {
        'input_data': pi21,
        'max_eng_group': 5,
        'max_ukr_group': 11,
    },
    'pi20': {
        'input_data': pi20,
        'max_eng_group': 5,
        'max_ukr_group': 10,
    },
    # 'pim22': {
    #     'input_data': pim22,
    #     'max_eng_group': 6,
    #     'max_ukr_group': None,
    # },
}


class GroupNumbers:
    def __init__(self, max_eng_group, max_ukr_group):
        self.eng = ','.join(map(str, range(1, max_eng_group + 1)))

        if max_ukr_group:
            self.ukr = ','.join(map(str, range(max_eng_group + 1,
                                                      max_ukr_group + 1)))
            self.all = f'{self.eng},{self.ukr}'
        else:
            self.ukr = None
            self.all = self.eng


class PotokParser:
    def __init__(self, potok, input_data, max_eng_group, max_ukr_group):
        self.potok = potok
        self.numbers = GroupNumbers(max_eng_group, max_ukr_group)
        self.parse(input_data)

    def parse(self, input_data):
        print('=' * 110, self.potok)
        for line in input_data.strip().split('\n'):
            SubjectParser(line, self.numbers)


class SubjectParser:
    def __init__(self, line, numbers):
        self.numbers = numbers
        self.parse_line(line)

    def parse_line(self, line):
        m = re.fullmatch(r'(?P<short>[^\t]+)\t'
                         r'(?P<long>.+) : '
                         r'(?P<other>.*)',
                         line)
        if not m:
            raise Exception(f'Wrong line format: "{line}"')

        short, long, other = m.groups()
        if short in ['ФВ', 'ІМ']:
            return  # skip because no teachers there

        print('-' * 100)
        print(short, '-', long)
        print('-' * 100)

        grouped_teachers = self.group_teachers(short, long, other)
        teachers_data = self.get_teachers_data(grouped_teachers)
        teachers_data = self.join_pz_and_lb(teachers_data)
        out_data = self.get_out_data(teachers_data)
        print(out_data)

    def group_teachers(self, short, long, other):
        grouped_teachers = defaultdict(lambda: defaultdict(list))

        for item in other.split(':'):
            item = item.strip()
            if not item:
                continue

            m = re.fullmatch(r'(?P<kind>Лк|Пз|Лб|Конс|Екз|Зал) '
                             r'\(\d+\) - '
                             r'(?P<groups>.+?), '
                             r'(?P<teachers>.*)',
                             item)
            if not m:
                raise Exception(f'Wrong item format: "{item}"')

            kind, groups, teachers = m.groups()
            if kind in ['Конс', 'Екз', 'Зал']:
                continue

            alternative = (
                short.startswith('*') and '*' in groups and '(' in groups
                or
                long.startswith('*') and '(' in groups
            )
            if alternative:
                groups = ['0']

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
        return grouped_teachers

    def get_teachers_data(self, grouped_teachers):
        teachers_data = defaultdict(dict)
        for teacher, data in grouped_teachers.items():
            for kind, groups in data.items():
                groups = ','.join(map(str, sorted(map(int, set(groups)))))
                if groups == self.numbers.ukr:
                    groups = 'ukr'
                else:
                    if self.numbers.ukr:
                        if groups == self.numbers.eng:
                            groups = 'eng'
                        elif groups == self.numbers.all:
                            groups = 'all'
                    else:
                        if groups == self.numbers.eng:
                            groups = 'all'
                teachers_data[teacher][kind] = groups

        # pprint(teachers_data)
        return teachers_data

    def join_pz_and_lb(self, teachers_data):
        for teacher, data in teachers_data.items():
            if 'Лб' in data:
                if data.get('Лб') == data.get('Пз'):
                    value = data['Лб']
                    del data['Лб']
                    del data['Пз']
                    data['Пз-Лб'] = value

        # pprint(teachers_data)
        return teachers_data

    def get_out_data(self, teachers_data):
        result = ''
        for teacher, data in teachers_data.items():
            values = ', '.join([
                f"{kind}-{groups}".lower()
                for kind, groups in data.items()
            ])
            result += f'{teacher}: {values}\n'

        return result


if __name__ == '__main__':
    for potok, data in potoks.items():
        PotokParser(potok, **data)
