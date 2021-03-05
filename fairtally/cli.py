import io
import sys
import click
from howfairis import Checker
from howfairis import Compliance
from howfairis import Repo
from tqdm import tqdm
from fairtally.get_badge_color import get_badge_color
from fairtally.redirect_stdout_stderr import RedirectStdStreams
from fairtally.utils import merge_urls
from fairtally.utils import write_as_html
from fairtally.utils import write_as_json


@click.command()
@click.argument("urls", nargs=-1)
@click.option("--output-file", "-o", "output_filename",
              help="Filename of where to write the results. Use `-` to write to standard out.",
              default="tally.html", show_default=True)
@click.option("--input-file", "-i", "input_file",
              help="Check URLs in file. One URL per line. Use `-` to read from standard input.",
              default=None,
              type=click.File('rt'))
@click.option("--format", "output_format",
              help="Format of output",
              default="html", show_default=True,
              type=click.Choice(("html", "json")))
def cli(urls, input_file, output_format, output_filename):
    all_urls = merge_urls(urls, input_file)

    if len(all_urls) == 0:
        click.echo("No URLs provided, aborting.", err=True)
        sys.exit(1)

    results = list()

    url_progressbar = tqdm(all_urls, bar_format="fairtally progress: |{bar}| {n_fmt}/{total_fmt}", ncols=70, position=0)
    current_value = tqdm(total=0, bar_format="{desc}", position=1)
    for url in url_progressbar:
        stderr_buffer = io.StringIO()
        stdout_buffer = io.StringIO()
        with RedirectStdStreams(stdout=stdout_buffer, stderr=stderr_buffer):
            try:
                current_value.set_description_str("currently checking " + url)
                repo = Repo(url)
                compliance = Checker(repo, ignore_repo_config=True, is_quiet=True).check_five_recommendations()
            except Exception:
                compliance = Compliance(False, False, False, False, False)
            finally:
                badge = "https://img.shields.io/badge/fair--software.eu-{0}-{1}"\
                        .format(compliance.urlencode(), get_badge_color(compliance))
                d = dict(url=url, badge=badge, repository=compliance.repository, license=compliance.license,
                         registry=compliance.registry, citation=compliance.citation, checklist=compliance.checklist,
                         count=compliance.count(), stdout=stdout_buffer.getvalue(), stderr=stderr_buffer.getvalue())

        current_value.set_description_str()
        results.append(d)

    if output_filename == 'tally.html' and output_format == 'json':
        output_filename = 'tally.json'

    with click.open_file(output_filename, mode='wt') as output_file:
        if output_format == 'html':
            write_as_html(results, output_file)
        elif output_format == 'json':
            write_as_json(results, output_file)
        else:
            click.echo("Unsupported format", err=True)
            sys.exit(1)

    click.echo(f'Completed checks on {len(all_urls)} URLs results written to {output_filename}', err=True)
