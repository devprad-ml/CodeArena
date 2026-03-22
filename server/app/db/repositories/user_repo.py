from typing import Optional, Dict, Any

from bson import ObjectId

from app.db.mongodb import get_database
from app.models.user import User


class UserRepository:
    def __init__(self):
        self.collection_name = "users"

    @property
    def collection(self):
        return get_database()[self.collection_name]

    async def create(self, user: User) -> User:
        """Create a new user"""
        user_dict = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return User(**doc)
        return None

    async def get_by_provider(
        self, provider: str, provider_id: str
    ) -> Optional[User]:
        """Get user by OAuth provider and provider ID"""
        doc = await self.collection.find_one(
            {"provider": provider, "provider_id": provider_id}
        )
        if doc:
            doc["_id"] = str(doc["_id"])
            return User(**doc)
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        doc = await self.collection.find_one({"email": email})
        if doc:
            doc["_id"] = str(doc["_id"])
            return User(**doc)
        return None

    async def update(
        self, user_id: str, update_data: Dict[str, Any]
    ) -> Optional[User]:
        """Update user fields"""
        await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return await self.get_by_id(user_id)
