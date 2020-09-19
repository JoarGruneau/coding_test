import pymongo


def get_keys(col):
    result = col.aggregate([{
        "$project": {
            "arrayofkeyvalue": {
                "$objectToArray": "$$ROOT"
            }
        }
    }, {
        "$unwind": "$arrayofkeyvalue"
    }, {
        "$group": {
            "_id": None,
            "allkeys": {
                "$addToSet": "$arrayofkeyvalue.k"
            }
        }
    }])
    for res in result:
        return res['allkeys']
    return []


def get_stats(col, key):
    result = col.aggregate([{
        '$match': {
            key: {
                '$exists': True
            }
        }
    }, {
        '$group': {
            '_id': f'${key}',
            'count': {
                '$sum': 1
            }
        }
    }, {
        "$group": {
            "_id": None,
            "counts": {
                "$push": {
                    "k": "$_id",
                    "v": "$count"
                }
            }
        }
    }, {
        "$replaceRoot": {
            "newRoot": {
                "$arrayToObject": "$counts"
            }
        }
    }])
    for res in result:
        return res
    return {}
