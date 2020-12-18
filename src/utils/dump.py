from shared_utils.io.json import json_dump_changed, json_dump

from src.utils.filename import get_filenames
from src.utils.slack import slack_status


def dump_json_data(path, potok_slug, kind, names, values):
    for data_slug, data_value in zip(names, values):
        active_filename, backup_filename = \
            get_filenames(path, f'{potok_slug}_{data_slug}', 'json')

        if json_dump_changed(active_filename, data_value):
            slack_status(f'{kind} changed: {data_slug}')
            json_dump(backup_filename, data_value)
