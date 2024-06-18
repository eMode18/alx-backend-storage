#!/usr/bin/env python3
"""
Provides a function insert_school that inserts a new document in a pymongo collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a collection based on kwargs.

    :param mongo_collection: pymongo collection object
    :param kwargs: key-value pairs to be inserted as document fields
    :return: the new _id of the inserted document
    """
    if not kwargs:
        return None
    return mongo_collection.insert_one(kwargs).inserted_id
