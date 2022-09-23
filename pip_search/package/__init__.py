from textwrap import dedent

import attr
from bs4 import Tag
from colorama import init, Style, Fore

init(autoreset=True)


@attr.s(kw_only=True, frozen=True, slots=True, auto_attribs=True)
class Package:
    """
    Class that contains data about a package
    """

    name: str
    version: str
    description: str

    @classmethod
    def from_package_snippet(cls, package_snippet: Tag) -> "Package":
        """
        Parses out package details from a pypi snippet
        """
        name = package_snippet.find(attrs={"class": "package-snippet__name"}).text
        version = package_snippet.find(attrs={"class": "package-snippet__version"}).text
        description = package_snippet.find(
            attrs={"class": "package-snippet__description"}
        ).text

        assert name is not None
        assert version is not None
        assert description is not None

        return cls(name=name, version=version, description=description)

    def __str__(self) -> str:
        return f"{self.name} {self.version}\n" f"    {self.description}"

    def color_output(self) -> str:
        """
        Returns colourized version of __str__
        """
        return (
            f"{Style.BRIGHT + self.name} {Fore.GREEN + self.version}\n"
            f"    {Style.RESET_ALL + self.description}"
        )
