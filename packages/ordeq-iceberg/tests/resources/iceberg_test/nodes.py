from resources.iceberg_test.catalog import my_catalog, my_save_table, test_namespace
from ordeq import node
from pyiceberg.catalog import Catalog
from pyiceberg.table import Table

@node(inputs=[my_catalog, test_namespace], outputs=[my_save_table])
def create_save_table(catalog: Catalog, namespace: str) -> Catalog:
    catalog.create_namespace(namespace)

@node(inputs=[my_catalog, my_save_table])
def load_table(catalog: Catalog, save_table: Table):
    loaded_table = catalog.load_table("test_namespace.new_test_table")
    print("Table loaded from catalog is:", loaded_table.schema())
    print(save_table.schema) # Raises error "AttributeError: 'NoneType' object has no attribute 'schema'"
