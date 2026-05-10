import asyncio

from app.core.database import SessionLocal
from app.seed.seed_data import run_seed


async def _main() -> None:
    async with SessionLocal() as session:
        await run_seed(session)


if __name__ == "__main__":
    asyncio.run(_main())
