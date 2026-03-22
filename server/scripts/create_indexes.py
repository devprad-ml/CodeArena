"""Create MongoDB indexes for optimal query performance"""

import asyncio

from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database


async def create_indexes():
    """Create all necessary indexes"""
    await connect_to_mongo()
    db = get_database()

    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index([("provider", 1), ("provider_id", 1)], unique=True)

    # Problems indexes
    await db.problems.create_index("slug", unique=True)
    await db.problems.create_index([("path", 1), ("difficulty", 1)])
    await db.problems.create_index([("path", 1), ("category", 1)])

    # Submissions indexes
    await db.submissions.create_index([("user_id", 1), ("submitted_at", -1)])
    await db.submissions.create_index([("user_id", 1), ("problem_id", 1)])

    # UserProgress indexes
    await db.user_progress.create_index("user_id", unique=True)

    print("All indexes created successfully!")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(create_indexes())
