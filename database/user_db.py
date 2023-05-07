from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import DATABASE_NAME, DATABASE_URL


class Database:
    "It's a wrapper for the pymongo library that allows you to interact with a MongoDB database"

    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db['users']

    async def create_user(self, user_id: int):
        user = {
            "user_id": user_id,
            "banned": False
        }
        result = await self.users.insert_one(user)
        return result.inserted_id

    async def update_user(self, user_id: int, data, tag="set"):
        result = await self.users.update_one(
            {"user_id": user_id}, {f"${tag}": data}
        )
        return result.modified_count

    async def find_user(self, user_id: int):
        "Returns a user document if found, else returns None"
        return await self.users.find_one({"user_id": user_id})

    async def filter_user(self, value):
        users = self.users.find(value)
        return [user["user_id"] async for user in users]

    async def ban_user(self, user_id: int):
        user = await self.find_user(user_id)
        if user:
            user["banned"] = True
            result = await self.users.update_one(
                {"user_id": user_id}, {"$set": user}
            )
            return result.modified_count
        else:
            return None

    async def get_total_users(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def get_user_ids(self):
        cursor = self.users.find({}, {"user_id": 1})
        return [user["user_id"] async for user in cursor]

    async def unban_user(self, user_id: int):
        user = await self.find_user(user_id)
        if user or user["banned"]:
            user["banned"] = False
            result = await self.users.update_one(
                {"user_id": user_id}, {"$set": user}
            )
            return result.modified_count
        else:
            return None

    async def delete_user(self, user_id: int):
        result = await self.users.delete_one({"user_id": user_id})
        return result.deleted_count

    async def user_exists(self, user_id: int):
        user = await self.users.find_one({"user_id": user_id})
        return user is not None

    async def get_banned_user_ids(self):
        cursor = self.users.find({"banned": True}, {"user_id": 1})
        return [user["user_id"] async for user in cursor]


print("Connecting to database... ")
db = Database(DATABASE_URL, DATABASE_NAME)
print("Connected to database!")
