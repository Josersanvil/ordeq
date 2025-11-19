import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from ordeq_viz_cli import main, parse_args


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (
            (
                "--package",
                "example1.a1",
                "--fmt",
                "kedro",
                "--output",
                "output_dir",
            ),
            {
                "packages": ["example1.a1"],
                "fmt": "kedro",
                "output": Path("output_dir"),
            },
        ),
        (
            (
                "--package",
                "example1.a1",
                "example2.a2",
                "--fmt",
                "kedro",
                "--output",
                "output_dir",
            ),
            {
                "packages": ["example1.a1", "example2.a2"],
                "fmt": "kedro",
                "output": Path("output_dir"),
            },
        ),
        (
            (
                "--package",
                "example1.a1",
                "--fmt",
                "mermaid",
                "--output",
                "output_dir",
            ),
            {
                "packages": ["example1.a1"],
                "fmt": "mermaid",
                "output": Path("output_dir"),
            },
        ),
        (
            # This test case checks that the parser only parses known args.
            (
                "--package",
                "example1.a1",
                "--fmt",
                "mermaid",
                "--output",
                "output_dir",
                "--unknown-arg",
                "value",
            ),
            {
                "packages": ["example1.a1"],
                "fmt": "mermaid",
                "output": Path("output_dir"),
            },
        ),
    ],
)
def test_it_parses(args, expected):
    assert vars(parse_args(args)) == expected


@patch("ordeq_viz_cli.viz")
def test_it_calls_viz(mocked_viz: MagicMock):
    with patch.object(
        sys,
        "argv",
        [
            "ordeq-viz",
            "--package",
            "example1.a1",
            "--fmt",
            "kedro",
            "--output",
            "output_dir",
        ],
    ):
        main()
    mocked_viz.assert_called_once_with(
        "example1.a1", output=Path("output_dir"), fmt="kedro"
    )


@patch("ordeq_viz_cli.viz")
def test_it_calls_viz_when_no_output(mocked_viz: MagicMock):
    with (
        patch.object(
            sys,
            "argv",
            [
                "ordeq-viz",
                "--package",
                "example1.a1",
                "--fmt",
                "mermaid",
                "--output",
                "-",
            ],
        ),
        patch.object(sys, "stdout") as mocked_stdout,
    ):
        main()
    mocked_viz.assert_called_once_with(
        "example1.a1", output=None, fmt="mermaid"
    )
    mocked_stdout.write.assert_called_once()
    mocked_stdout.flush.assert_called_once()
