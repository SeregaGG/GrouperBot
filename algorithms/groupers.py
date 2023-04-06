import datetime
from dateutil.relativedelta import relativedelta


async def group_by(group_type: str, dt_from: datetime.datetime, dt_upto: datetime.datetime, db):
    current_format = "%Y-%m-%dT%H:00:00"
    current_period = int((dt_upto - dt_from).total_seconds() // 3600)
    if group_type == "day":
        current_format = "%Y-%m-%dT00:00:00"
        current_period = (dt_upto - dt_from).days

    if group_type == "month":
        current_format = "%Y-%m-01T00:00:00"
        current_period = (dt_upto.year - dt_from.year) * 12 + dt_upto.month - dt_from.month

    document = db.sample_collection.aggregate([
        {"$match": {
            "dt": {"$gte": dt_from, "$lte": dt_upto}
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": current_format, "date": "$dt"}},
            "count": {"$sum": "$value"}
        }},
        {"$sort": {"_id": 1}}
    ])
    dataset_labels = []
    dataset = []
    async for doc in document:
        dataset_labels.append((doc.get('count'), doc.get('_id')))
        dataset.append(doc.get('_id'))

    for interval in range(current_period + 1):

        if group_type == "day":
            if not (dt_from + datetime.timedelta(days=interval)).strftime("%Y-%m-%dT%H:%M:%S") in dataset:
                dataset_labels.append((0, (dt_from + datetime.timedelta(days=interval)).strftime("%Y-%m-%dT%H:%M:%S")))

        if group_type == "hour":
            if not (dt_from + datetime.timedelta(hours=interval)).strftime("%Y-%m-%dT%H:%M:%S") in dataset:
                dataset_labels.append((0, (dt_from + datetime.timedelta(hours=interval)).strftime("%Y-%m-%dT%H:%M:%S")))

        if group_type == "month":
            if not (dt_from + relativedelta(months=current_period)).strftime("%Y-%m-01T%H:%M:%S") in dataset:
                dataset_labels.append(
                    (0, (dt_from + relativedelta(months=current_period)).strftime("%Y-%m-%dT%H:%M:%S")))

    dataset_labels.sort(key=lambda x: datetime.datetime.strptime(x[1], "%Y-%m-%dT%H:%M:%S"))

    dataset = [x[0] for x in dataset_labels]
    labels = [x[1] for x in dataset_labels]

    return {'dataset': dataset, 'labels': labels}
