from aiofiles import open
from os import PathLike, path
from typing import Union

import threading
import os
import json
import warnings


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




class CacheObject:
    """CacheObject class can be regarded as a memory database.
    It is a singleton class, which means there is only one instance of it.

    Example:
        >>> cache = CacheObject('cache.json')
        >>> cache.set('key','value')
        >>> cache.get('key')
        'value'
        >>> cache.remove('key')
        >>> cache.get('key')
        None

    Attributes:
        _cache (dict): cache dictionary
        _mutex (threading.Lock): mutex lock
        _localdb (os.PathLike): local database file path

    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CacheObject, cls).__new__(cls)
        return cls._instance

    def __init__(self, localdb: os.PathLike = None) -> None:
        """Contructor of CacheObject class.
        Args:
            localdb (os.PathLike): local database file path
        """
        self._cache = dict()
        self._mutex = threading.Lock()
        self._localdb = localdb
        if self._localdb is not None:
            with self._mutex:
                self._load()

    def _load(self):
        if os.path.exists(self._localdb):
            with open(self._localdb) as f:
                self._cache = json.load(f)
        else:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def set(self, key, value):
        if key in self._cache:
            warnings.warn('Key already exists, will be overwritten.')
        self._cache[key] = value

    def get(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
            return None
        return self._cache[key]

    def remove(self, key):
        if key not in self._cache:
            warnings.warn('Key not found.')
        del self._cache[key]

    def clear(self):
        self._cache.clear()

    def submit(self):
        if self._localdb is None:
            warnings.warn('Local database not specified.')
            return
        # with lock
        with self._mutex:
            with open(self._localdb, 'w+') as f:
                json.dump(self._cache, f)

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
        self.submit()
    