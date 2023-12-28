from aioredis import Redis, ConnectionPool

from config import appcfg


async def sys_cache() -> Redis:
    """
    系统缓存,只能存储字符
    :return: cache 生成一个连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = ConnectionPool.from_url(
        appcfg.CACHE_URL,
        db=appcfg.CACHE_DB_IDX.get('system'),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)

async def code_cache() -> Redis:
    """
    可存储任意
    :return:
    """
    bin_cache_pool = ConnectionPool.from_url(
        appcfg.CACHE_URL,
        db=appcfg.CACHE_DB_IDX.get('bin')
    )
    return Redis(connection_pool=bin_cache_pool)
