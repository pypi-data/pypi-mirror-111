from django.db.models.query import QuerySet


def db_update(db_data, data_dict: dict = dict()):
    assert isinstance(db_data, QuerySet) \
        or (hasattr(db_data, '_meta') and hasattr(db_data._meta, 'model'))
    assert isinstance(data_dict, dict)

    dataset = db_data if isinstance(db_data, QuerySet) else [db_data]
    for single_data in dataset:
        for key, value in data_dict.items():
            if hasattr(single_data, key):
                setattr(single_data, key, value)
        single_data.save()
    return dataset
