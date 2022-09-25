from uuid import uuid4
from textwrap import dedent
import json

from bs4 import BeautifulSoup
from colorama import init, Style, Fore
import hypothesis

from pip_search.package import Package, PackageEncoder

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


@hypothesis.given(
    name=hypothesis.strategies.builds(lambda: str(uuid4())),
    version=hypothesis.strategies.builds(lambda: str(uuid4())),
    description=hypothesis.strategies.builds(lambda: str(uuid4())),
)
def test_from_package_snippet(name: str, version: str, description: str) -> None:
    """
    Tests `Package.from_package_snippet`'s parsing
    """
    soup = BeautifulSoup(
        f"""
        <a class="package-snippet" href="/project/{name}/">
            <h3 class="package-snippet__title">
                <span class="package-snippet__name">{name}</span>
                <span class="package-snippet__version">{version}</span>
                <span class="package-snippet__created"><time data-controller="localized-time" data-localized-time-relative="true" data-localized-time-show-time="false" datetime="2022-07-28T13:20:27+0000">
                    Jul 28, 2022
                </time></span>
            </h3>
            <p class="package-snippet__description">{description}</p>
        </a>
        """,
        features="html5lib",
    )
    pkg = Package.from_package_snippet(soup)
    assert pkg.name == name
    assert pkg.version == version
    assert pkg.description == description


@hypothesis.given(
    name=hypothesis.strategies.builds(lambda: str(uuid4())),
    version=hypothesis.strategies.builds(lambda: str(uuid4())),
    description=hypothesis.strategies.builds(lambda: str(uuid4())),
)
def test_encode_package(name: str, version: str, description: str) -> None:
    """
    Tests `PackageEncoder` class
    """
    pkg = Package(name=name, version=version, description=description)

    pkg_json = json.dumps(pkg, cls=PackageEncoder)
    deserialized_pkg = json.loads(pkg_json)
    assert deserialized_pkg["name"] == name
    assert deserialized_pkg["version"] == version
    assert deserialized_pkg["description"] == description
