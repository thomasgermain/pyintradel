from __future__ import annotations

from typing import Any, Dict

from bs4 import BeautifulSoup


def parse(response: str) -> list[Any]:
    """Parse response from intradel"""
    results = []
    soup = BeautifulSoup(response, features="html.parser")

    if soup.find(attrs={"name": "pLogin"}) is not None:
        raise ValueError("Wrong response received, login/password seems incorrect", response)

    content = (
        soup.find(attrs={"class": "grid"})
        .find(attrs={"class": "row"})
        .findChildren(attrs={"class": "post__content"})
    )
    for data in content:
        result: Dict[str, Any] = {}
        if data.find(name="h3") is not None:
            name = _name(data)
            start_date = _start_date(data)
            chip_id = _chip_id(data) or name
            details = _details(data)
            total = _total(data) or str(len(details))

            result.update({"name": name})
            result.update({"start_date": start_date})
            result.update({"id": chip_id})
            result.update({"details": details})
            result.update({"total": total})
            results.append(result)

    return results


def _name(data: BeautifulSoup) -> str:
    return str(data.find(name="h3").text.strip())


def _start_date(data: BeautifulSoup) -> str:
    info = data.findAll(name="p")
    start_date = info[0]
    if len(info) > 1:
        start_date = info[3]

    return str(start_date.text.split(":")[1].strip())


def _chip_id(data: BeautifulSoup) -> str | None:
    chip_id = None
    possible_chip_id = data.findChildren(name="p")
    if len(possible_chip_id) > 1:
        chip_id = str(data.findChildren(name="p")[1].text.split(":")[1].strip())
    return chip_id


def _details(data: BeautifulSoup) -> list[Any]:
    attrs = []
    for row in data.find(name="tbody").findChildren(name="tr"):
        tds = row.findAll(name="td")
        attrs.append({"date": tds[0].text, "detail": tds[2].text})
    return attrs


def _total(data: BeautifulSoup) -> str | None:
    total = None
    possible_total = data.find(name="tfoot").findChildren("td")
    if possible_total:
        total = str(possible_total[2].text.split(" ")[0].strip())
    return total
