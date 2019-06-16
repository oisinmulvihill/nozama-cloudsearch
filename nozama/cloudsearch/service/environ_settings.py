import os


def get(var, default, type_=None):
    """Return a function to recover latest env variable contents."""
    def _env_getter():
        """Recover the latest setting from the environment."""
        val = os.environ.get(var, default)
        if type_:
            val = type_(val)
        return val
    return _env_getter


MONGO_DBNAME = get('MONGO_DBNAME', 'nozama-cloudsearch')
MONGO_HOST = get('MONGO_HOST', 'localhost')
MONGO_PORT = get('MONGO_PORT', 27017, int)

ELASTICSEARCH_HOST = get('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = get('ELASTICSEARCH_PORT', 9200, int)
