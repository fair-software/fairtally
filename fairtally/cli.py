import io
import json
import click
from howfairis import Checker
from howfairis import Repo
from howfairis import Compliance
from tqdm import tqdm
from fairtally.get_badge_color import get_badge_color
from fairtally.redirect_stdout_stderr import RedirectStdStreams


@click.command()
@click.argument("urls", nargs=-1)
def cli(urls=None):

    if urls is None:
        print("No URLs provided, aborting.")
        return

    stderr_buffer = io.StringIO()
    stdout_buffer = io.StringIO()
    results = list()

    url_progressbar = tqdm(urls, bar_format="fairtally progress: |{bar}| {n_fmt}/{total_fmt} | {desc}")
    for url in url_progressbar:

        with RedirectStdStreams(stdout=stdout_buffer, stderr=stderr_buffer):
            try:
                url_progressbar.set_description_str(url)
                repo = Repo(url)
                checker = Checker(repo, ignore_repo_config=True, is_quiet=True)
                compliance = checker.check_five_recommendations()
            except Exception:
                compliance = Compliance(False, False, False, False, False)
            finally:
                badge = "https://img.shields.io/badge/fair--software.eu-{0}-{1}"\
                        .format(compliance.urlencode(), get_badge_color(compliance))
                d = dict(url=url, badge=badge, repository=compliance.repository, license=compliance.license,
                         registry=compliance.registry, citation=compliance.citation, checklist=compliance.checklist,
                         count=compliance.count(), stdout=stdout_buffer.getvalue(), stderr=stderr_buffer.getvalue())

        results.append(d)
        url_progressbar.set_description_str()

    print(json.dumps(results))


if __name__ == "__main__":
    cli()
