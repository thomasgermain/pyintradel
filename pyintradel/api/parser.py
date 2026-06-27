from typing import Any

from bs4 import BeautifulSoup, NavigableString, Tag


def parse(response: str) -> list[Any]:
    """Parse response from intradel"""
    results: list[Any] = []
    soup = BeautifulSoup(response, features="html.parser")

    if soup.select_one('[name="pLogin"]') is not None:
        raise ValueError("Wrong response received, login/password seems incorrect", response)

    for data in soup.select(".grid .row .post__content"):
        result: dict[str, Any] = {}
        if data.find("h3") is not None:
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


def _require_tag(node: Tag | NavigableString | None) -> Tag:
    """Narrow a bs4 lookup result to a Tag, failing loudly on unexpected markup."""
    if not isinstance(node, Tag):
        raise ValueError("Unexpected response structure from intradel")
    return node


def _name(data: Tag) -> str:
    return _require_tag(data.find("h3")).text.strip()


def _start_date(data: Tag) -> str:
    info = data.find_all("p")
    start_date = info[0]
    if len(info) > 1:
        start_date = info[3]

    return start_date.text.split(":")[1].strip()


def _chip_id(data: Tag) -> str | None:
    chip_id = None
    possible_chip_id = data.find_all("p")
    if len(possible_chip_id) > 1:
        chip_id = possible_chip_id[1].text.split(":")[1].strip()
    return chip_id


def _details(data: Tag) -> list[Any]:
    attrs = []
    for row in _require_tag(data.find("tbody")).find_all("tr"):
        tds = row.find_all("td")
        # When the list is empty, the website still includes an empty row.
        # Let's just skip empty rows, as a valid row needs a date anyway.
        if tds[0].text:
            attrs.append({"date": tds[0].text, "detail": tds[2].text})
    return attrs


def _total(data: Tag) -> str | None:
    total = None
    possible_total = _require_tag(data.find("tfoot")).find_all("td")
    if possible_total:
        total = possible_total[2].text.split(" ")[0].strip()
    return total
