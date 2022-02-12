from coda.lib import Coda

import conf


coda = Coda('timetable', '2022-1', conf.coda_token)

coda_records = coda.table('Расписание')
coda_subjects = coda.table('Предметы')
coda_groups = coda.table('Группы')
