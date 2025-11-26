from dataclasses import dataclass
from typing import Any

import polars as pl
from ordeq import IO, Input

try:
    from pyiceberg.table import Table
except ImportError:

    class Table:  # type: ignore[no-redef]
        ...  # Placeholder if pyiceberg is not installed


@dataclass(frozen=True, kw_only=True)
class PolarsLazyIceberg(IO[pl.LazyFrame]):
    """IO for loading Iceberg tables lazily using Polars.

    Example:

    ```pycon
    >>> from ordeq_polars import PolarsLazyIceberg
    >>> iceberg = PolarsLazyIceberg(
    ...     path="file:/path/to/iceberg-table/metadata.json",
    ... )

    ```

    """

    path: str | Table | Input[Table | str]

    def load(self, **load_options: Any) -> pl.LazyFrame:
        """Load an Iceberg table.

        Args:
            **load_options: Additional options passed to pl.read_iceberg.

        Returns:
            LazyFrame containing the Iceberg table data
        """
        if isinstance(self.path, Input):
            source = self.path.load()
        else:
            source = self.path
        return pl.scan_iceberg(source=source, **load_options)
