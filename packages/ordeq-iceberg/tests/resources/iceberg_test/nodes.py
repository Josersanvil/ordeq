from resources.iceberg_test.catalog import my_catalog, my_load_table, my_save_table, test_namespace
from ordeq import node
from pyiceberg.catalog import Catalog
from pyiceberg.table import Table

@node(inputs=[my_catalog, test_namespace], outputs=[my_save_table])
def create_save_table(catalog: Catalog, namespace: str) -> Catalog:
    catalog.create_namespace(namespace)
    return catalog

@node(inputs=[my_save_table])
def load_table(save_table: Table):
    print("Table is loaded")
    print(save_table.schema)
