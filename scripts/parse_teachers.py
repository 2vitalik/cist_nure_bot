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


def get_groups_numbers_texts(max_eng_group, max_ukr_group):
    eng_groups_text = ','.join(map(str, range(1, max_eng_group + 1)))

    if max_ukr_group:
        ukr_groups_text = ','.join(map(str, range(max_eng_group + 1,
                                                  max_ukr_group + 1)))
        all_groups_text = f'{eng_groups_text},{ukr_groups_text}'
    else:
        ukr_groups_text = None
        all_groups_text = eng_groups_text

    return eng_groups_text, ukr_groups_text, all_groups_text


class Parser:
    def __init__(self, potok, input_data, max_eng_group, max_ukr_group):
        self.potok = potok
        self.input_data = input_data
        self.eng_groups_text, self.ukr_groups_text, self.all_groups_text = \
            get_groups_numbers_texts(max_eng_group, max_ukr_group)
        self.parse()

    def parse(self):
        print('=' * 110, self.potok)
        for line in self.input_data.strip().split('\n'):
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
        self.print_data(teachers_data)

    def group_teachers(self, short, long, other):
        grouped_teachers = defaultdict(lambda: defaultdict(list))

        for item in other.split(':'):
            item = item.strip()
            if not item:
                continue
            m = re.fullmatch(r'(Лк|Пз|Лб|Конс|Екз|Зал) \(\d+\) - (.+?), (.*)', item)
            if not m:
                print(item)
                raise Exception('Failed `fullmatch`')
            kind, groups, teachers = m.groups()

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
                try:
                    print(groups)
                    groups = ','.join(map(str, sorted(map(int, set(groups)))))
                except ValueError as e:
                    print(e)
                    print(groups)
                    raise e
                if groups == self.ukr_groups_text:
                    groups = 'ukr'
                else:
                    if self.ukr_groups_text:
                        if groups == self.eng_groups_text:
                            groups = 'eng'
                        elif groups == self.all_groups_text:
                            groups = 'all'
                    else:
                        if groups == self.eng_groups_text:
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

    def print_data(self, teachers_data):
        for teacher, data in teachers_data.items():
            values = ', '.join([
                f"{kind}-{groups}".lower()
                for kind, groups in data.items()
            ])
            print(f'{teacher}: {values}')


if __name__ == '__main__':
    for potok, data in potoks.items():
        Parser(potok, **data).parse()
