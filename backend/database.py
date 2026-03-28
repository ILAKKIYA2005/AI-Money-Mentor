import uuid
import os
import json
from datetime import datetime

class MockCollection:
    def __init__(self, name, db_instance):
        self.name = name
        self.db = db_instance

    def _get_data(self):
        return self.db.full_data.get(self.name, {})

    def _save_data(self, collection_data):
        self.db.full_data[self.name] = collection_data
        self.db.save()

    async def find_one(self, query):
        data = self._get_data()
        for item in data.values():
            match = True
            for k, v in query.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                return item
        return None

    async def insert_one(self, document):
        data = self._get_data()
        if "_id" not in document:
            document["_id"] = str(uuid.uuid4())
        data[document["_id"]] = document
        self._save_data(data)
        return type('obj', (object,), {'inserted_id': document["_id"]})

    async def update_one(self, query, update):
        data = self._get_data()
        item = None
        for i in data.values():
            match = True
            for k, v in query.items():
                if i.get(k) != v:
                    match = False
                    break
            if match:
                item = i
                break
        
        if item:
            if "$set" in update:
                item.update(update["$set"])
            self._save_data(data)
        return type('obj', (object,), {'modified_count': 1 if item else 0})

    async def delete_one(self, query):
        data = self._get_data()
        item = await self.find_one(query)
        if item:
            del data[item["_id"]]
            self._save_data(data)
        return type('obj', (object,), {'deleted_count': 1 if item else 0})

    def find(self, query):
        class Cursor:
            def __init__(self, data):
                self.data = list(data)
            async def __aiter__(self):
                for item in self.data:
                    yield item
            async def to_list(self, length):
                return self.data[:length]
        
        data = self._get_data()
        results = []
        for item in data.values():
            match = True
            for k, v in query.items():
                if str(item.get(k)) != str(v):
                    match = False
                    break
            if match:
                results.append(item)
        return Cursor(results)

class MockDatabase:
    def __init__(self):
        self.file_path = "mock_db.json"
        self.full_data = self.load()
        self.users = MockCollection("users", self)
        self.expenses = MockCollection("expenses", self)

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"users": {}, "expenses": {}}

    def save(self):
        def datetime_handler(x):
            if isinstance(x, datetime):
                return x.isoformat()
            raise TypeError("Unknown type")
            
        with open(self.file_path, "w") as f:
            json.dump(self.full_data, f, default=datetime_handler)

db = MockDatabase()

async def get_database():
    return db

async def test_db_connection():
    return True
