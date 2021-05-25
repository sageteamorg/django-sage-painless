import uuid


def create_cache_key(include_data: list):
    """
    Generate cache key contains the argument data
    """
    cache_key = str()
    for data in include_data:
        cache_key += f'{uuid.uuid4()}-{data}'
    return cache_key
