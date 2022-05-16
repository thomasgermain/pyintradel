# pyIntradel

![PyPI - License](https://img.shields.io/github/license/thomasgermain/pyIntradel)
![PyPI](https://img.shields.io/pypi/v/pyIntradel)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyIntradel.svg)

A python connector for waste collection for province of Liège. This connector is using screen scraping to collect
following data (for the current year), in json:
- "Green bin" (organic waste) and "black bin" residual waste
  - Total weight
  - Number of collections
  - details of all the collections
  - chip number
  - starting date (01/01 of the current year)
- Recypark
  - details of all the visits
  - (01/01 of the current year)

Here is an example of json:

```json
[
    {
        "name": "ORGANIQUE",
        "start_date": "01-01-2022",
        "id": "123456",
        "details":
        [
            {
                "date": "20-01-2022",
                "detail": "34.0"
            },
            {
                "date": "17-02-2022",
                "detail": "27.0"
            },
            {
                "date": "07-04-2022",
                "detail": "36.0"
            }
        ],
        "total": "97"
    },
    {
        "name": "RESIDUEL",
        "start_date": "01-01-2022",
        "id": "78810",
        "details":
        [
            {
                "date": "20-01-2022",
                "detail": "14.5"
            },
            {
                "date": "07-04-2022",
                "detail": "11.5"
            },
            {
                "date": "21-04-2022",
                "detail": "11.5"
            }
        ],
        "total": "37.5"
    },
    {
        "name": "RECYPARC",
        "start_date": "01-01-2022",
        "id": "RECYPARC",
        "details":
        [
            {
                "date": "14-04-2022",
                "detail": "Encombrants (0.35 m³), Petits Bruns (0.00 pièce)"
            }
        ],
        "total": "1"
    }
]
```

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
python3 main.py user passw town
```

---
<a href="https://www.buymeacoffee.com/tgermain" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
