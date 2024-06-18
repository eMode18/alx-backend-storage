#!/usr/bin/env python3
"""
Provides a function schools_by_topic that finds schools by
topic in a pymongo collection.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of school having a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: topic searched
    :return: list of schools with the specific topic
    """
    return list(mongo_collection.find({"topics": topic}))
