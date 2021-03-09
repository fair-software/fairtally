import sys
import click
from tqdm import tqdm
from fairtally import __version__
from fairtally.check import check_url
from fairtally.utils import merge_urls
from fairtally.utils import write_as_html
from fairtally.utils import write_as_json


DEFAULT_OUTPUT_FILENAME = "tally.html"


@click.command('fairtally')
@click.argument("urls", nargs=-1)
@click.option("--output-file", "-o", "output_filename",
              help="Filename of where to write the results. Use `-` to write to standard out.",
              default=DEFAULT_OUTPUT_FILENAME, show_default=True)
@click.option("--input-file", "-i", "input_file",
              help="Check URLs in file. One URL per line. Use `-` to read from standard input.",
              default=None,
              type=click.File("rt"))
@click.option("--format", "output_format",
              help="Format of output.",
              default="html", show_default=True,
              type=click.Choice(("html", "json")))
@click.version_option(__version__)
def cli(urls, input_file, output_format, output_filename):
    all_urls = merge_urls(urls, input_file)

    if len(all_urls) == 0:
        click.echo("No URLs provided, aborting.", err=True)
        sys.exit(1)

    url_progressbar = tqdm(all_urls, bar_format="fairtally progress: |{bar}| {n_fmt}/{total_fmt}", ncols=70, position=0)
    current_value = tqdm(total=0, bar_format="{desc}", position=1)
    results = [check_url(url, current_value) for url in url_progressbar]

    if output_filename == DEFAULT_OUTPUT_FILENAME and output_format == "json":
        output_filename = "tally.json"

    with click.open_file(output_filename, mode="wt") as output_file:
        if output_format == "html":
            write_as_html(results, output_file)
        elif output_format == "json":
            write_as_json(results, output_file)
        else:
            click.echo("Unsupported format", err=True)
            sys.exit(1)

    msg = f"Completed fairtally on {len(all_urls)} URLs and written report to {output_filename}"
    current_value.set_description_str(msg)
