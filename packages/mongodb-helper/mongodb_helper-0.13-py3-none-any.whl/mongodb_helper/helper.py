from .errors import *
from pymongo.collection import Collection

class Helper:
    """
    Methods that simplify MongoDB collection reading and writing.


    id_structure
                - must be a string
                - example of an id_structure: "_id": 1122334455667788
                  _id is the id_structure in this case ^
    collection
                - must be a pymongo.collection.Collection

    Every method except delete_document will return a dictionary of the document.

    get_document reads a document with the given id
    update_document updates the documents data with the given id
    insert_document creates a new document with the given id and data
    delete_document deletes a document with the given id
    """

    def __init__(self, id_structure: str, collection: Collection):
        self.id_structure = id_structure
        self.collection = collection

    # Returns a dictionary with the data of the document
    def get_document(self, id: int):
        return self.collection.find_one({self.id_structure: id})

    # Returns a dictionary with the data of the updated document
    def update_document(self, id: int, data: dict):
        self.collection.update_one({self.id_structure: id}, {"$set": data})
        return self.get_document(id)

    # Returns a dictionary with the data of the inserted document
    def insert_document(self, id: int, data: dict):
        data[self.id_structure] = id
        self.collection.insert_one(data)
        return self.get_document(id)

    # Make sure to wrap the method call in a try block as it can raise an error if the document with the id could not be found
    def delete_document(self, id: int):
        document = self.get_document(id)
        if document is None:
            raise DocumentNotFoundError(f"Document with the id {id} could not be found.")
        self.collection.delete_one({self.id_structure: id})
