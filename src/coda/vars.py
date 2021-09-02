from coda.lib import Coda

import conf


coda = Coda('cist_nure', '2021-2', conf.coda_token)

coda_records = coda.table('Расписание')
coda_subjects = coda.table('Предметы')
coda_groups = coda.table('Группы')
