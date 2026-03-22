"""Database migration utilities"""

import asyncio

from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database


async def run_migrations():
    """Run database migrations"""
    await connect_to_mongo()
    db = get_database()

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index([("provider", 1), ("provider_id", 1)], unique=True)
    await db.problems.create_index("slug", unique=True)
    await db.problems.create_index([("path", 1), ("difficulty", 1)])
    await db.problems.create_index("category")
    await db.submissions.create_index([("user_id", 1), ("problem_id", 1)])
    await db.submissions.create_index("submitted_at")

    print("Migrations complete!")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(run_migrations())
