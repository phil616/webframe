
import aiofiles

async def write_to_path(file: bytes, path: str):
    async with aiofiles.open(path, "wb+") as f:
        await f.write(file)


async def read_from_path(filepath: str):
    async with aiofiles.open(filepath, "rb") as f:
        return f.read()
