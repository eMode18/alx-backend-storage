#!/usr/bin/env python3
"""
Provides a function list_all that lists all documents in a pymongo collection.
"""

from typing import List


def list_all(mongo_collection) -> List:
    """
    List all documents in a collection.

    :param mongo_collection: pymongo collection object
    :return: list of documents in the collection, or an empty list if no document
    """
    return list(mongo_collection.find()) if mongo_collection else []
