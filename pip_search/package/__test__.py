from uuid import uuid4
from textwrap import dedent

from bs4 import BeautifulSoup
from colorama import init, Style, Fore
import hypothesis

from pip_search.package import Package

init(autoreset=True)


@hypothesis.given(
    name=hypothesis.strategies.builds(lambda: str(uuid4())),
    version=hypothesis.strategies.builds(lambda: str(uuid4())),
    description=hypothesis.strategies.builds(lambda: str(uuid4())),
)
def test_str(name: str, version: str, description: str) -> None:
    """
    Tests `Package.__str__`'s formatting
    """
    pkg = Package(name=name, version=version, description=description)
    assert str(pkg) == f"{name} {version}\n" f"    {description}"


@hypothesis.given(
    name=hypothesis.strategies.builds(lambda: str(uuid4())),
    version=hypothesis.strategies.builds(lambda: str(uuid4())),
    description=hypothesis.strategies.builds(lambda: str(uuid4())),
)
def test_color_output(name: str, version: str, description: str) -> None:
    """
    Tests `Package.color_output`'s formatting
    """
    pkg = Package(name=name, version=version, description=description)
    assert (
        pkg.color_output() == f"{Style.BRIGHT + name} {Fore.GREEN + version}\n"
        f"    {Style.RESET_ALL + description}"
    )


def test_from_package_snippet() -> None:
    """
    Tests `Package.from_package_snippet`'s parsing
    """
    soup = BeautifulSoup()
