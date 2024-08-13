#!/usr/bin/env python3
"""
students
"""


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,  # Include the student's name
                "averageScore": {  # Calculate average score
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {  # Sort by average score in descending order
                "averageScore": -1
            }
        }
    ])
