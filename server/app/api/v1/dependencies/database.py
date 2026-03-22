from app.db.mongodb import get_database


async def get_db():
    """Database session dependency"""
    return get_database()
