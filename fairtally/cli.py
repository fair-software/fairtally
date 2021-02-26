import io

import click
from howfairis import Checker, Repo
from tqdm import tqdm

from fairtally.get_badge_color import get_badge_color
from fairtally.redirect_stdout_stderr import RedirectStdStreams


@click.command()
@click.argument("urls", nargs=-1)
def cli(urls):

    stderr_buffer = io.StringIO()
    stdout_buffer = io.StringIO()
    results = list()
    bar_format = "fairtally progress: |{bar}| {n_fmt}/{total_fmt}"
    for url in tqdm(urls, bar_format=bar_format, ncols=70):
        repo = Repo(url)

        with RedirectStdStreams(stdout=stdout_buffer, stderr=stderr_buffer):
            checker = Checker(repo, ignore_repo_config=True, is_quiet=True)
            compliance = checker.check_five_recommendations()
            badge = "https://img.shields.io/badge/fair--software.eu-{0}-{1}"\
                    .format(compliance.urlencode(), get_badge_color(compliance))
            d = dict(url=url, badge=badge, repository=compliance.repository, license=compliance.license,
                     registry=compliance.registry, citation=compliance.citation, checklist=compliance.checklist,
                     count=compliance.count(), stdout=stdout_buffer.getvalue(), stderr=stderr_buffer.getvalue())

        results.append(d)

    print(results)


if __name__ == "__main__":
    cli([])
