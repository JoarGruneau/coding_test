import argparse
import pprint
from datetime import datetime

import pandas as pd
import pymongo
from numpy import nan

from queries import get_keys, get_stats

REPORT_FIELDS = [
    'Type of mobile', 'Navigational status', 'Ship type', 'Cargo type'
    'Type of position fixing device', 'Data source type'
]


def get_db(db):
    return pymongo.MongoClient("mongodb://localhost:27017/")[db]


def get_documents(csv_file):
    data = pd.read_csv(file_name)
    data['Timestamp'] = pd.to_datetime(data['# Timestamp'])
    del data['# Timestamp']
    data = data.replace(['Unknown', 'Unknown value', 'Undefined'], nan)
    documents = data.T.apply(lambda x: x.dropna().to_dict()).tolist()
    return data.keys(), documents


def get_report(col):
    fields = get_keys(col)
    report = {'timestamp': datetime.now().timestamp()}
    report['missing_count'] = {
        field: col.count_documents({field: {
            '$exists': False
        }})
        for field in fields
    }
    report['stats'] = {key: get_stats(col, key) for key in REPORT_FIELDS}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='*', help='csv files to load')
    args = parser.parse_args()

    db = get_db('code_test')
    col = get_db('code_test')['ships']

    print('Loading data files...')
    if args.files:
        for file_name in args.files:
            fields, documents = get_documents(file_name)
            indexes = [
                pymongo.IndexModel([(field, pymongo.ASCENDING)], sparse=True)
                for field in fields
            ]
            col.create_indexes(indexes)
            col.insert_many(documents)

    report = get_report(col)
    print('Generated report:')
    printer = pprint.PrettyPrinter(indent=4)
    printer.pprint(report)
    print('Saving report...')
    db['reports'].insert_one(report)
