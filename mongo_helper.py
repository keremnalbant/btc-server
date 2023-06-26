import os

import motor.motor_asyncio


class MongoHelper:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = self.get_client
        self.db = self.get_db()
        self.collection = self.get_collection()

    @property
    def get_client(self):
        return motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DB_URI'))

    def get_db(self):
        return self.client[self.db_name]

    def get_collection(self):
        return self.db[self.collection_name]

    async def insert_one(self, data):
        return await self.collection.insert_one(data)

    async def insert_many(self, data):
        return await self.collection.insert_many(data)

    async def find_one(self, query):
        return await self.collection.find_one(query)

    async def find_many(self, query):
        cursor = self.collection.find(query)
        return await cursor.to_list(length=None)

    async def delete_one(self, query):
        return await self.collection.delete_one(query)

    async def delete_many(self, query):
        return await self.collection.delete_many(query)

    async def update_one(self, query, data):
        return await self.collection.update_one(query, data)

    async def update_many(self, query, data):
        return await self.collection.update_many(query, data)

    async def count(self, query):
        return await self.collection.count(query)

    async def distinct(self, field, query):
        return await self.collection.distinct(field, query)

    async def aggregate(self, query):
        cursor = self.collection.aggregate(query)
        return await cursor.to_list(length=None)

    async def count_documents(self, query):
        return await self.collection.count_documents(query)

    async def find_all(self):
        cursor = self.collection.find()
        return await cursor.to_list(length=None)
