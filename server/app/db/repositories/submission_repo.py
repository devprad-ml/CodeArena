from typing import Optional, List, Dict, Any

from bson import ObjectId

from app.db.mongodb import get_database
from app.models.submission import Submission


class SubmissionRepository:
    def __init__(self):
        self.collection_name = "submissions"

    @property
    def collection(self):
        return get_database()[self.collection_name]

    async def create(self, submission: Submission) -> Submission:
        """Create a new submission"""
        sub_dict = submission.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(sub_dict)
        submission.id = str(result.inserted_id)
        return submission

    async def get_by_id(self, submission_id: str) -> Optional[Submission]:
        """Get submission by ID"""
        doc = await self.collection.find_one({"_id": ObjectId(submission_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Submission(**doc)
        return None

    async def get_by_user(
        self, user_id: str, skip: int = 0, limit: int = 20
    ) -> List[Submission]:
        """Get submissions by user"""
        cursor = (
            self.collection.find({"user_id": user_id})
            .sort("submitted_at", -1)
            .skip(skip)
            .limit(limit)
        )
        submissions = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            submissions.append(Submission(**doc))
        return submissions

    async def update(
        self, submission_id: str, update_data: Dict[str, Any]
    ) -> Optional[Submission]:
        """Update submission fields"""
        await self.collection.update_one(
            {"_id": ObjectId(submission_id)}, {"$set": update_data}
        )
        return await self.get_by_id(submission_id)

    async def count_attempts(self, user_id: str, problem_id: str) -> int:
        """Count number of attempts for a problem by user"""
        return await self.collection.count_documents(
            {"user_id": user_id, "problem_id": problem_id}
        )
