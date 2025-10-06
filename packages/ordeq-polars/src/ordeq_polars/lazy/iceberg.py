from __future__ import annotations

from dataclasses import dataclass

import polars as pl
from ordeq import IO
from ordeq_iceberg import IcebergTable


@dataclass(frozen=True, kw_only=True)
class PolarsLazyIcebergTable(IO[pl.LazyFrame]):
    """IO for loading and saving Iceberg tables lazily using Polars."""

    table: IcebergTable

    def load(self, **load_options) -> pl.LazyFrame:
        return pl.scan_iceberg(self.table.load(), **load_options)

    def save(self, df: pl.LazyFrame | pl.DataFrame, **save_options) -> None:
        df.write_iceberg(self.table.load(), **save_options)


@dataclass(frozen=True, kw_only=True)
class PolarsEagerIcebergTable(PolarsLazyIcebergTable[IO[pl.DataFrame]]):
    """IO for loading and saving Iceberg tables eagerly using Polars."""

    table: IcebergTable

    def load(self, **load_options) -> pl.DataFrame:
        lazy_df = super().load(**load_options)
        return lazy_df.collect()
