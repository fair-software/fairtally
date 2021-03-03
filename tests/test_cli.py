import pytest
import requests_mock
from click.testing import CliRunner
from fairtally.cli import cli


@pytest.fixture
def mocked_internet():
    with requests_mock.Mocker() as m:
        repo = "https://github.com/fair-software/repo1"
        raw = "https://raw.githubusercontent.com/fair-software/repo1"
        api = "https://api.github.com/repos/fair-software/repo1"
        m.get(api, status_code=200, json={"default_branch": "master"})
        m.get(api + "/license", status_code=200)
        m.get(raw + "/master/.howfairis.yml", status_code=404)
        m.get(raw + "/master/.zenodo.json", status_code=404)
        m.get(raw + "/master/CITATION.cff", status_code=404)
        m.get(raw + "/master/CITATION", status_code=404)
        m.get(raw + "/master/codemeta.json", status_code=404)
        m.get(raw + "/master/README.rst", status_code=404)
        m.get(raw + "/master/README.md", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/.howfairis.yml", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/.zenodo.json", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/CITATION.cff", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/CITATION", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/codemeta.json", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/README.md", status_code=404)
        m.get(raw + "/master/this/path/does-not-exist/README.rst", status_code=404)
        m.get(repo, status_code=200, text="<html>GitHub page for repo1</html>")
        return m


@pytest.fixture
def invoke_cli(mocked_internet):
    runner = CliRunner()

    def _invoker(args):
        with mocked_internet:
            return runner.invoke(cli, args, catch_exceptions=False)

    return _invoker


def test_singleurl_nooptions(invoke_cli):
    result = invoke_cli("https://github.com/fair-software/repo1")
    assert "fairtally progress" in result.output
