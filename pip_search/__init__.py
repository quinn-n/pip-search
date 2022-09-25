from typing import Optional
import json

import click
from colorama import init, Style, Fore

from pip_search.query import query_pypi
from pip_search.package import Package, PackageEncoder


init(autoreset=True)


def print_human_readable_output(
    packages: list[Package], total_packages: int, page: int, color_output: bool
) -> None:
    """
    Prints human-readable output
    """
    RESULTS_PER_PAGE = 20

    start_result = (page - 1) * RESULTS_PER_PAGE
    end_result = page * RESULTS_PER_PAGE
    if end_result > total_packages:
        end_result = total_packages

    if color_output:
        click.echo(
            f"Showing results {Fore.BLUE + str(start_result) + Style.RESET_ALL} to {Fore.BLUE + str(end_result) + Style.RESET_ALL} of {Fore.BLUE + str(total_packages) + Style.RESET_ALL}. Use -p to change pages."
        )
    else:
        click.echo(
            f"Showing results {start_result} to {end_result} of {total_packages}. Use -p to change pages."
        )

    for package in packages:
        if color_output:
            click.echo(package.color_output())
        else:
            click.echo(package)


def print_json_output(packages: list[Package]) -> None:
    """
    Prints machine-readable json output
    """
    click.echo(json.dumps(packages, cls=PackageEncoder))


@click.command()
@click.option(
    "-p", "--page", required=False, type=int, help="Get a specific page", default=1
)
@click.option("--no-color-output", is_flag=True, help="Disables colorized output")
@click.option("-j", "--json", is_flag=True, help="Outputs computer-readable JSON")
@click.argument("search_terms", required=True, type=str, nargs=-1)
def pip_search(
    search_terms: list[str], page: int, no_color_output: bool, json: bool
) -> None:
    """Queries pip and prints the results"""

    packages, total_packages = query_pypi(search_terms, page)
    if json:
        print_json_output(packages)
    else:
        print_human_readable_output(packages, total_packages, page, not no_color_output)
