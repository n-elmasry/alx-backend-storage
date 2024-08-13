#!/usr/bin/env python3
"""top_students"""
import pymongo


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    students = mongo_collection.find().sort("averageScore", pymongo.DESCENDING)
    return list(students)
