from shared_utils.common.dt import dtf


def get_filenames(path, slug, ext):  # todo: move to `shared_utils`
    active_filename = f'{path}/{slug}.{ext}'
    day_slug = dtf('Ymd')  # todo: make customizable via args
    time_slug = dtf('dts')
    backup_filename = \
        f'{path}/{day_slug}/{slug}_{time_slug}.{ext}'
    return active_filename, backup_filename
