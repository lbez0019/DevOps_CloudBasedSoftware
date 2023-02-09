import os
import tempfile
import pymongo

from functools import reduce
#from tinydb import TinyDB, Query

mongoClient = pymongo.MongoClient("mongodb://mongo:27017/")
mydb = mongoClient["mydatabase"]
collection = mydb["students"]

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)


def add(student=None):
    queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)
    student_id = collection.count_documents({}) + 1

    query = { "first_name": student.first_name, "last_name": student.last_name }
    res = collection.count_documents(query)
    #res = student_db.search(query)
    if res > 0:
        return 'already exists', 409

    student = student.to_dict()
    student.update({"student_id": student_id})
    collection.insert_one(student)

    return student_id

def get_by_id(student_id=None, subject=None):
    #student = student_db.get(doc_id=int(student_id))
    student = collection.find_one({"student_id": student_id})

    if not student:
        return 'not found', 404

    #print(student)
    student['_id'] = str(student['_id'])
    return student

def delete(student_id=None):
    student = collection.find({"student_id": int(student_id)})
    if not student:
        return 'not found', 404
    #student_db.remove(doc_ids=[int(student_id)])
    collection.delete_one({"student_id": int(student_id)})
    return student_id


