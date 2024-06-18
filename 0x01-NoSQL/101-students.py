#!/usr/bin/env python3
"""
Module to work with students in MongoDB.
"""


def top_students(mongo_collection):
    """ Return all students sorted by average score. """
    # Aggregate pipeline to calculate the average and sort by it
    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    # Execute the aggregation pipeline
    top_students_list = list(mongo_collection.aggregate(pipeline))
    return top_students_list
