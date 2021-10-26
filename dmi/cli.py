import click
import os


@click.group()
def dmi():
    """Command line interface for DMI API"""


@dmi.group()
def lightning():
    """Access to lightning data"""


@lightning.command()
@click.argument("DATE_BEGIN")
@click.argument("DATE_END")
@click.option("--output", "-o",
              help="Path to output file; default: write to stdout")
@click.option("--api-key", "-k",
              default=lambda: os.environ.get("DMI_API_KEY"),
              help="API key; default: read from DMI_API_KEY env var")
def download(output, api_key, date_begin, date_end):
    """
    Download a set of lightning strike events.

    Date range is limited to between DATE_BEGIN and DATE_END (both inclusive).

    Output is CSV (comma-separated, UTF-8, Unix line breaks, no headers).
    One row per lightning strike event with the following columns:

    \b
    1. timestamp (ISO 8601 UTC)
    2. longitude (triangulated position)
    3. latitude (triangulated position)
    4. lightning type (see https://confluence.govcloud.dk/pages/viewpage.action?pageId=37355739)
    """
    if not api_key:
        click.get_current_context().fail("No API key specified")

    raise NotImplementedError("TODO")
