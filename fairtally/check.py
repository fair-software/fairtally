import io
from howfairis import Checker
from howfairis import Compliance
from howfairis import Repo
from fairtally.get_badge_color import get_badge_color
from fairtally.redirect_stdout_stderr import RedirectStdStreams


def check_url(url, current_value):
    stderr_buffer = io.StringIO()
    stdout_buffer = io.StringIO()
    with RedirectStdStreams(stdout=stdout_buffer, stderr=stderr_buffer):
        try:
            current_value.set_description_str("currently checking " + url)
            repo = Repo(url)
            compliance = Checker(repo, ignore_repo_config=True, is_quiet=True).check_five_recommendations()
        except Exception:
            compliance = Compliance(False, False, False, False, False)

        badge = "https://img.shields.io/badge/fair--software.eu-{0}-{1}" \
            .format(compliance.urlencode(), get_badge_color(compliance))
        return dict(url=url, badge=badge, repository=compliance.repository, license=compliance.license,
                    registry=compliance.registry, citation=compliance.citation, checklist=compliance.checklist,
                    count=compliance.count(), stdout=stdout_buffer.getvalue(), stderr=stderr_buffer.getvalue())
