import asyncio
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_seed.db"
from app.core.db import create_db_and_tables, seed_db_if_empty

async def main():
    await create_db_and_tables()
    await seed_db_if_empty()
    print("OK")

asyncio.run(main())
