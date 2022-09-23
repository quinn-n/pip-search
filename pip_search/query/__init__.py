from bs4 import BeautifulSoup
import requests
import string

from pip_search.package import Package


def query_pypi(search_terms: list[str], page: int) -> tuple[list[Package], int]:
    """
    Queries pypi and returns a list of packages
    Returns:
        tuple(list[Package], int): Returns the packages for the page and the *total* number of results for the search
    """
    search_query = " ".join(search_terms)
    resp = requests.get(
        "https://pypi.org/search/", params={"q": search_query, "page": page}
    )

    assert (
        resp.status_code == 200
    ), f"pypi returned a non-200 status code {resp.status_code}"

    soup = BeautifulSoup(resp.text, features="html5lib")
    snippets = soup.find_all(attrs={"class": "package-snippet"})
    total_packages = get_total_packages(soup)

    packages = [Package.from_package_snippet(snippet) for snippet in snippets]

    return packages, total_packages


def get_total_packages(soup: BeautifulSoup) -> int:
    """
    Returns the number of packages on a search page
    """
    raw_num_str = soup.find("strong").text

    num_str = "".join([c if c in string.digits else "" for c in raw_num_str])

    return int(num_str)
