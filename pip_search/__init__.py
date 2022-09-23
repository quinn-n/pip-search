from typing import Optional

import click
from colorama import init, Style, Fore

from pip_search.query import query_pypi


init(autoreset=True)


@click.command()
@click.option(
    "-p", "--page", required=False, type=int, help="Results page number", default=1
)
@click.option("--no-color-output", is_flag=True, help="Disables colorized output")
@click.argument("search_terms", required=True, type=str, nargs=-1)
def pip_search(search_terms: list[str], page: int, no_color_output: bool) -> None:
    """Queries pip and prints the results"""

    RESULTS_PER_PAGE = 20

    packages, total_packages = query_pypi(search_terms, page)

    start_result = (page - 1) * RESULTS_PER_PAGE
    end_result = page * RESULTS_PER_PAGE
    if end_result > total_packages:
        end_result = total_packages

    if no_color_output:
        click.echo(
            f"Showing results {start_result} to {end_result} of {total_packages}. Use -p to change pages."
        )
    else:
        click.echo(
            f"Showing results {Fore.BLUE + str(start_result) + Style.RESET_ALL} to {Fore.BLUE + str(end_result) + Style.RESET_ALL} of {Fore.BLUE + str(total_packages) + Style.RESET_ALL}. Use -p to change pages."
        )

    for package in packages:
        if no_color_output:
            click.echo(package)
        else:
            click.echo(package.color_output())
