# pylint: disable=missing-function-docstring       # not a requirement for functions that are tests
# pylint: disable=redefined-outer-name             # need this to be able to use fixtures

import pytest
import requests_mock
from click.testing import CliRunner

from fairtally import __version__
from fairtally.cli import cli


@pytest.fixture
def mocked_internet():
    with requests_mock.Mocker() as mocker:
        repo = "https://github.com/fair-software/repo1"
        raw = "https://raw.githubusercontent.com/fair-software/repo1"
        api = "https://api.github.com/repos/fair-software/repo1"
        mocker.get(api, status_code=200, json={"default_branch": "master"})
        mocker.get(api + "/license", status_code=200)
        mocker.get(raw + "/master/.howfairis.yml", status_code=404)
        mocker.get(raw + "/master/.zenodo.json", status_code=404)
        mocker.get(raw + "/master/CITATION.cff", status_code=404)
        mocker.get(raw + "/master/CITATION", status_code=404)
        mocker.get(raw + "/master/codemeta.json", status_code=404)
        mocker.get(raw + "/master/README.rst", status_code=404)
        mocker.get(raw + "/master/README.md", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/.howfairis.yml", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/.zenodo.json", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/CITATION.cff", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/CITATION", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/codemeta.json", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/README.md", status_code=404)
        mocker.get(raw + "/master/this/path/does-not-exist/README.rst", status_code=404)
        mocker.get(repo, status_code=200, text="<html>GitHub page for repo1</html>")
        return mocker


@pytest.fixture
def cli_runner():
    return CliRunner(mix_stderr=False)


@pytest.fixture
def invoke_cli(mocked_internet, cli_runner):
    def _invoker(args, **kwargs):
        with mocked_internet:
            return cli_runner.invoke(cli, args, catch_exceptions=False, **kwargs)

    return _invoker


def test_help(invoke_cli):
    result = invoke_cli("--help")
    assert "Usage: fairtally" in result.stdout


def test_version(invoke_cli):
    result = invoke_cli("--version")
    assert __version__ in result.stdout


def test_no_url(invoke_cli):
    result = invoke_cli("")

    assert "No URLs provided, aborting." in result.stderr
    assert result.exit_code == 1


def read_file(filename):
    with open(filename, "r") as fid:
        return fid.read()


def test_single_url_no_options(invoke_cli, cli_runner: CliRunner):
    with cli_runner.isolated_filesystem():
        url = "https://github.com/fair-software/repo1"
        result = invoke_cli(url)

        assert "fairtally progress" in result.stderr
        assert "Completed fairtally on 1 URLs and written report to tally.html" in result.stderr
        assert result.exit_code == 0
        assert url in read_file("tally.html")


def test_input_from_file_to_stdout(invoke_cli, tmp_path):
    my_input_file = tmp_path / "urls.txt"
    my_input_file.write_text("https://github.com/fair-software/repo1\n")

    result = invoke_cli(["--input-file", str(my_input_file), "--output-file", "-"])

    assert "fairtally progress" in result.stderr
    assert "Completed fairtally on 1 URLs and written report to -" in result.stderr
    assert result.exit_code == 0
    assert "https://github.com/fair-software/repo1" in result.stdout


def test_input_from_stdin_to_stdout(invoke_cli):
    stdin = "https://github.com/fair-software/repo1\n"

    result = invoke_cli(["--input-file", "-", "--output-file", "-"], input=stdin)

    assert "fairtally progress" in result.stderr
    assert "Completed fairtally on 1 URLs and written report to -" in result.stderr
    assert result.exit_code == 0
    assert "https://github.com/fair-software/repo1" in result.stdout


def test_json_format(invoke_cli, cli_runner):
    with cli_runner.isolated_filesystem():
        url = "https://github.com/fair-software/repo1"
        result = invoke_cli([url, "--format", "json"])

        assert "fairtally progress" in result.stderr
        assert "Completed fairtally on 1 URLs and written report to tally.json" in result.stderr
        assert result.exit_code == 0
        assert url in read_file("tally.json")


def test_json_format_to_stdout(invoke_cli):
    url = "https://github.com/fair-software/repo1"
    result = invoke_cli([url, "--format", "json", "--output-file", "-"])

    assert "fairtally progress" in result.stderr
    assert "Completed fairtally on 1 URLs and written report to -" in result.stderr
    assert result.exit_code == 0
    assert url in result.stdout
