from aiofiles import open
from os import PathLike, path
from typing import Union


async def write_to_local(file: bytes, filename: PathLike):
    if path.exists(filename):
        # warning : file overwrite
        ...
    fp = await open(filename, "wb")
    await fp.write(file)


async def read_by_filename(filename: PathLike) -> Union[bytes, None]:
    if not path.exists(filename):
        return None
    fp = await open(filename, 'rb')
    filebytes = await fp.read()
    return filebytes
