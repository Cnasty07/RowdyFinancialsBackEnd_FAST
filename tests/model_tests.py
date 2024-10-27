import unittest
from pymongo import MongoClient
import os

from database.models import MyModel  # Adjust the import based on your actual model and file structure

class TestMongoDBModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the MongoDB client and database
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['test_database']
        cls.collection = cls.db['test_collection']
        cls.model = MyModel(cls.db)  # Initialize your model with the database

    @classmethod
    def tearDownClass(cls):
        # Clean up the database after tests
        cls.client.drop_database('test_database')
        cls.client.close()

    def test_insert_document(self):
        # Test inserting a document using the model
        document = {"name": "John Doe", "age": 30}
        result = self.model.insert_document(document)
        self.assertIsNotNone(result.inserted_id)

    def test_find_document(self):
        # Test finding a document using the model
        document = {"name": "Jane Doe", "age": 25}
        self.model.insert_document(document)
        found_document = self.model.find_document({"name": "Jane Doe"})
        self.assertIsNotNone(found_document)
        self.assertEqual(found_document['name'], "Jane Doe")
        self.assertEqual(found_document['age'], 25)

    def test_update_document(self):
        # Test updating a document using the model
        document = {"name": "John Smith", "age": 40}
        self.model.insert_document(document)
        self.model.update_document({"name": "John Smith"}, {"$set": {"age": 41}})
        updated_document = self.model.find_document({"name": "John Smith"})
        self.assertEqual(updated_document['age'], 41)

    def test_delete_document(self):
        # Test deleting a document using the model
        document = {"name": "Jane Smith", "age": 35}
        self.model.insert_document(document)
        self.model.delete_document({"name": "Jane Smith"})
        deleted_document = self.model.find_document({"name": "Jane Smith"})
        self.assertIsNone(deleted_document)

def main():
    unittest.main()


if __name__ == '__main__':
    main()