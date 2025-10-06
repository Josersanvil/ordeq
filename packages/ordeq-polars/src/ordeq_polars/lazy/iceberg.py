from __future__ import annotations

from dataclasses import dataclass

import polars as pl
from ordeq.framework.io import IO, Input
from pyiceberg.table import Table


@dataclass(frozen=True, kw_only=True)
class PolarsLazyIcebergTable(IO[pl.LazyFrame]):
    """IO for loading and saving Iceberg tables lazily using Polars."""

    table: Input[Table] | Table

    def _get_table(self) -> Table:
        if isinstance(self.table, Input):
            return self.table.load()
        return self.table

    def load(self, **load_options) -> pl.LazyFrame:
        return pl.scan_iceberg(self._get_table(), **load_options)

    def save(self, df: pl.LazyFrame, **save_options) -> None:
        collected_df = df.collect()
        collected_df.write_iceberg(self._get_table(), **save_options)


@dataclass(frozen=True, kw_only=True)
class PolarsEagerIcebergTable(IO[pl.DataFrame]):
    """IO for loading and saving Iceberg tables eagerly using Polars."""

    table: Input[Table] | Table

    def _get_table(self) -> Table:
        if isinstance(self.table, Input):
            return self.table.load()
        return self.table

    def load(self, **load_options) -> pl.DataFrame:
        lazy_df = super().load(**load_options)
        return lazy_df.collect()

    def save(self, df: pl.DataFrame, **save_options) -> None:
        df.write_iceberg(self._get_table(), **save_options)
