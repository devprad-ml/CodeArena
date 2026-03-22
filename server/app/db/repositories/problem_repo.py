from typing import Optional, List, Dict, Any

from bson import ObjectId

from app.db.mongodb import get_database
from app.models.problem import Problem


class ProblemRepository:
    def __init__(self):
        self.collection_name = "problems"

    @property
    def collection(self):
        return get_database()[self.collection_name]

    async def create(self, problem: Problem) -> Problem:
        """Create a new problem"""
        problem_dict = problem.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(problem_dict)
        problem.id = str(result.inserted_id)
        return problem

    async def get_by_id(self, problem_id: str) -> Optional[Problem]:
        """Get problem by ID"""
        doc = await self.collection.find_one({"_id": ObjectId(problem_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Problem(**doc)
        return None

    async def get_by_slug(self, slug: str) -> Optional[Problem]:
        """Get problem by slug"""
        doc = await self.collection.find_one({"slug": slug})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Problem(**doc)
        return None

    async def get_random_by_criteria(
        self,
        path: str,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        exclude_solved_by: Optional[str] = None,
    ) -> Optional[Problem]:
        """Get a random problem matching criteria"""
        query: Dict[str, Any] = {"path": path}

        if difficulty:
            query["difficulty"] = difficulty
        if category:
            query["category"] = category

        pipeline = [{"$match": query}, {"$sample": {"size": 1}}]

        cursor = self.collection.aggregate(pipeline)
        docs = await cursor.to_list(length=1)

        if docs:
            doc = docs[0]
            doc["_id"] = str(doc["_id"])
            return Problem(**doc)
        return None

    async def get_by_path(
        self, path: str, skip: int = 0, limit: int = 20
    ) -> List[Problem]:
        """Get problems by path"""
        cursor = self.collection.find({"path": path}).skip(skip).limit(limit)
        problems = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            problems.append(Problem(**doc))
        return problems
