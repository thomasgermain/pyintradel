# pyIntradel

![PyPI - License](https://img.shields.io/github/license/thomasgermain/pyIntradel)
![PyPI](https://img.shields.io/pypi/v/pyIntradel)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyIntradel.svg)

A python connector for waste collection for province of Liège. This connector is using screen scraping to collect
following data (for the current year)
- "Green bin" (organic waste) and "black bin" residual waste
  - Total weight
  - Number of collections
  - details of all the collections
  - chip number
  - starting date (01/01 of the current year)
- Recypark
  - details of all the visits
  - (01/01 of the current year)

## Usage

The `town` parameter is the name of the town, you can check it here: [towns](pyintradel/api/towns.py)

### Python module

```python
import aiohttp
from pyintradel import api

async with aiohttp.ClientSession() as sess:
    await api.get_data(sess, login, password, town)
```

### Command line
```bash
python3 api.py user passw town
```

