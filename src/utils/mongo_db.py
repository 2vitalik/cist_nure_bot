from collections import defaultdict

from pymongo import MongoClient

import conf


class MongoDB:
    def __init__(self):
        self.client = MongoClient(conf.mongo_cluster_secret)
        self.db = self.client['nure_links']
        self.entries = EntriesTable(self.db['entries'])


class EntriesTable:
    def __init__(self, collection):
        self.collection = collection
        self.data = {}
        self.fetch()

    def fetch(self):
        self.data = defaultdict(lambda: defaultdict(list))
        entries = self.collection.find({'semester': conf.mongo_semester})
        for entry in entries:
            prefix = entry.get('prefix')
            subject = entry.get('subject')
            kind = entry.get('kind').split(',')
            groups = entry.get('groups').split(',')
            links = entry.get('links')
            self.data[prefix][subject].append((kind, groups, links))

    def get_links(self, prefix, subject, kind, group):
        entries = self.data[prefix][subject]
        links = []
        for _kind, _groups, _links in entries:  # todo: fix order (Загальне first)
            if (kind.capitalize() in _kind or _kind == ['*']) \
                    and (group in _groups or _groups == ['*'] or _groups == ['0']):
                if _links:
                    links.extend([link.strip() for link in _links.split('\n')])
        return links


db = MongoDB()
