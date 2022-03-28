from pymongo import MongoClient

def get_db (coleccion):
    MONGOURI = "mongodb://localhost"
    client = MongoClient(MONGOURI)
    db = client['temperaturatest']
    coleccion = db[coleccion]
    return coleccion