import os
from pathlib import Path

def get_database_uri():
    # filename = str(Path.home() / '//allocation.db')
    # filename = os.environ.get('DB_FILENAME', filename)
    # return f"sqlite://{filename}"

    host = os.environ.get('DB_HOST', 'localhost')
    port = 3306 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'allocation', 'allocation'

    return f'mysql://{user}:{password}@{host}:{port}/{db_name}'



    # host = os.environ.get('DB_HOST', 'localhost')
    # port = 54321 if host == 'localhost' else 5432
    # password = os.environ.get('DB_PASSWORD', 'abc123')
    # user, db_name = 'allocation', 'allocation'
    # return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get('API_HOST', 'localhost')
    port = 5005 if host == 'localhost' else 80
    return f"http://{host}:{port}"

