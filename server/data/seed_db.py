"""Database seeding script for initial problem data"""

import asyncio
import json
from pathlib import Path

from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database


async def seed_problems():
    """Seed problems from JSON files"""
    await connect_to_mongo()
    db = get_database()

    data_dir = Path(__file__).parent / "problems"

    # Seed DSA problems
    for difficulty in ["easy", "medium", "hard"]:
        filepath = data_dir / "dsa" / f"{difficulty}.json"
        if filepath.exists():
            with open(filepath) as f:
                problems = json.load(f)
                if problems:
                    for p in problems:
                        p["path"] = "pirate"
                        p["difficulty"] = difficulty
                    await db.problems.insert_many(problems)
                    print(f"Seeded {len(problems)} {difficulty} DSA problems")

    # Seed System Design problems
    for category in ["lld", "hld"]:
        filepath = data_dir / "system_design" / f"{category}.json"
        if filepath.exists():
            with open(filepath) as f:
                problems = json.load(f)
                if problems:
                    for p in problems:
                        p["path"] = "marine"
                        p["category"] = category
                    await db.problems.insert_many(problems)
                    print(f"Seeded {len(problems)} {category} problems")

    await close_mongo_connection()
    print("Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_problems())
