import os
import json

# _BASE_VERSION = '1.0'

# def get_next_version():
#     env = os.getenv('DSO_ENV') or 'prod'
#     if env == 'prod':
#         url = "https://pypi.org/pypi/dsocli/json"
#     else:
#         url = "https://test.pypi.org/pypi/dsocli/json"

#     versions = sorted(list(requests.get(url).json()['releases'].keys()), reverse=True)
#     if not versions: 
#         last_version = f"{_BASE_VERSION}.0"
#     else:
#         last_versions = versions[0]

#     major1, minor1, release1 = last_versions.split('.')
#     major2, minor2 = _BASE_VERSION.split('.')
#     if major2 == major1 and minor2 == minor1:
#         release2 = int(release1) + 1
#     else:
#         release2 = 1

#     return f"{major2}.{minor2}.{release2}"

with open(os.path.join(os.path.dirname(__file__), 'package.json')) as f:
    _info = json.load(f)

__version__ = _info['version']
