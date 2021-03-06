import json
from pathlib import Path
from typing import List
from typing import Set
from typing import TextIO


def merge_urls(urls: Set[str], input_file: TextIO) -> List[str]:
    """Merge URLs given as separate positional arguments and input file"""
    all_urls = list(urls)
    if input_file is not None:
        for line in input_file:
            url = line.strip()
            if url:
                all_urls.append(url)
    return all_urls


def write_as_html(results, output_file_html: TextIO):
    """Writes results to output file in HTML format"""
    parent = Path(__file__).parent
    template_file = parent / "data" / "index.html.template"
    with open(template_file) as fid:
        template_str = fid.read()
    report = template_str.replace("{{python inserts the data here}}", json.dumps(results))
    with output_file_html:
        output_file_html.write(report)


def write_as_json(results, output_file_json: TextIO):
    """Write results to output file in JSON format"""
    with output_file_json:
        json.dump(results, output_file_json, sort_keys=True)
