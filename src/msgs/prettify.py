from src.data.const import times


def prettify_lesson(subject, kind, room, comment, sep=' → '):
    icons = {
        'лк': '📖',
        'пз': '💬',
        'лб': '⚙️',
        'кс': '❓',
        'ісп': '💢',
    }
    icon = icons.get(kind, '❔')
    room_suffix = f'{sep}{room}' if room else ''
    comment_line = f'\n✍️ {comment}' if comment else ''
    return f'{icon} ({kind}) <b>{subject}</b>{room_suffix}{comment_line}'


def prettify_time_slot(day_table, time_key):
    lessons = day_table[time_key][::-1]
    number = times.get(time_key, '*️⃣')
    line = prettify_lesson(*lessons[0][1:])
    message = f'{number} <code>{time_key[:5]}</code>: {line}\n'
    for lesson in lessons[1:]:
        line = prettify_lesson(*lesson[1:])
        message += f'▫️<code>     </code>   {line}\n'
    return message
