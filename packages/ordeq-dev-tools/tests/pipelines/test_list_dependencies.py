"""Tests for the list_dependencies pipeline."""

from pathlib import Path
from ordeq import run
from ordeq_common import Literal

from ordeq_dev_tools.pipelines.list_dependencies import (
    compute_affected_dependencies,
)
from ordeq_dev_tools.pipelines.docs_package_overview import (
    groups,
    write_html_table_by_group,
    package_overview,
)
from ordeq_files import TextLinesStream


def test_compute_affected_dependencies():
    """Test the compute_affected_dependencies function."""
    deps_by_package = {
        "ordeq-a": [],
        "ordeq-b": ["ordeq-a"],
        "ordeq-c": ["ordeq-b"],
        "ordeq-d": ["ordeq-a", "ordeq-c"],
        "ordeq-e": [],
    }

    expected_affected = {
        "ordeq-a": ["ordeq-b", "ordeq-c", "ordeq-d"],
        "ordeq-b": ["ordeq-c", "ordeq-d"],
        "ordeq-c": ["ordeq-d"],
        "ordeq-d": [],
        "ordeq-e": [],
    }

    affected = compute_affected_dependencies(deps_by_package)

    assert affected == expected_affected


def test_write_html_table_by_group(tmp_path: Path):
    """Test the write_html_table_by_group function."""
    fp = tmp_path / "packages.md"
    tmp_package_overview = TextLinesStream(path=fp)
    run(
        write_html_table_by_group,
        io={
            groups: Literal[dict[str, list[dict[str, str | None]]]](
                {
                    "group1": [
                        {
                            "logo_url": "https://example.com/logo.png",
                            "pypi_name": "ordeq-sample",
                            "description": "A sample Ordeq package.",
                            "src_name": "ordeq_sample",
                            "pkg_dir": "ordeq-sample",
                        },
                        {
                            "logo_url": None,
                            "pypi_name": "ordeq-another",
                            "description": "Another Ordeq package.",
                            "src_name": "ordeq_another",
                            "pkg_dir": "ordeq-another",
                        },
                    ]
                }
            ),
            package_overview: tmp_package_overview,
        },
    )
    expected_content_path = Path(__file__).parent / "expected_packages.md"
    if not expected_content_path.exists():
        expected_content_path.write_text(fp.read_text())
    expected_content = expected_content_path.read_text()
    assert fp.read_text() == expected_content
