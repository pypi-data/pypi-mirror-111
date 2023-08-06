from copy import deepcopy
from enum import Enum
from typing import List, Dict, Tuple
from secyan_python.constant import E_role
from .column import Column, JoinColumn


class CharacterEnum(Enum):
    server = "SERVER"
    client = "CLIENT"

    @property
    def get_e_role(self) -> E_role:
        """
        This function will return the e_role based on the current value.
        Note that, e_role is a class from secyan c++.

        :return: E_role
        """

        if self == CharacterEnum.client:
            return E_role.CLIENT
        else:
            return E_role.SERVER


class Table:

    def __init__(self, table_name: str, columns: List[Column], data_sizes: List[float], data_paths: List[str],
                 annotations: List[str], owner: CharacterEnum = None):
        """
        Create a table with columns
        :param table_name: table name
        :param columns: list of columns
        :param data_sizes: list of sizes. Used for num_of_rows in the code
        :param annotations: List of annotations. Will use this field to fetch related annotation

        """

        assert len(data_paths) == len(data_sizes)

        self._table_name = table_name
        self.parent: "Table" = None
        self.data_paths = data_paths
        self.children: List["JoinColumn"] = []
        self.original_column_names: List[Column] = [
            Column(table=self, name=c.name, column_type=c.column_type) for c in
            columns
        ]
        self._owner = owner
        # Used for is_boolean struct
        self.is_bool = True
        self.used = False
        # This variable will be used for generating selected output.
        # None selected output will not be included in the final result
        self.used_in_select = False
        # List of fields used in select statement
        self.fields_used_in_select = []
        # This variable will be used for generating selection.
        # It will determine whether a table has been used during the operation
        self.used_in_join = False
        self.data_sizes = data_sizes
        self.annotations = annotations

    def __str__(self):
        return f"<Table: {self._table_name} />"

    @property
    def owner(self) -> CharacterEnum:
        """
        Get the owner of this table
        :return:
        """
        if self._owner:
            return self._owner
        else:
            depth = self.get_height()
            return CharacterEnum.server if depth % 2 == 1 else CharacterEnum.client

    def get_height(self) -> int:
        """
        Get max height of the join tree.

        For example,

        The height for tree
        ```
                a
              /    \
            b        c

        ```
        is 1

        The height for tree

        ```
                a
              /   \
            b       d
          /
        c

        ```
        is 2

        :return:
        """
        if len(self.children) == 0:
            return 0

        heights = []
        for c in self.children:
            t: "Table" = c.to_table
            heights.append(t.get_height())

        topmost = max(heights)

        return topmost + 1

    @staticmethod
    def load_from_json(json_content: dict) -> "Table":
        """
        Construct a table from json content
        :param json_content:
        :return:
        """
        assert "table_name" in json_content
        assert "columns" in json_content
        assert "data_sizes" in json_content
        assert "data_paths" in json_content
        assert "annotations" in json_content

        columns = [Column.load_column_from_json(c) for c in json_content['columns']]
        return Table(table_name=json_content["table_name"], columns=columns,
                     owner=CharacterEnum[json_content['owner']] if "owner" in json_content else None,
                     data_sizes=json_content['data_sizes'], data_paths=json_content['data_paths'],
                     annotations=json_content['annotations'])

    @property
    def variable_table_name(self) -> str:
        """
        Get a table's variable name. Used in codegen.
        For example, customer

        :return:
        """
        return self._table_name.lower()

    @property
    def relational_name(self) -> str:
        """
        Get relational name.

        :return:
        """
        return self._table_name.upper()

    @property
    def column_names(self):
        """
        Will return list of column names. However, this will not apply aggregate function.
        :return:
        """
        if len(self.children) == 0:
            return self.original_column_names
        else:
            column_names = [c for c in self.original_column_names]
            for join_column in self.children:
                for column_name in join_column.to_table.column_names:
                    column_names.append(column_name)

            # merge join fields
            for join_column in self.children:
                for i, column_name in enumerate(column_names):
                    if column_name.name == join_column.to_table_key and column_name.table == join_column.to_table:
                        del column_names[i]
                        break

            return column_names

    def get_columns_after_aggregate(self) -> List[Column]:
        """
        Get list of columns after aggregation. This will include all columns passed from children
        and it's columns
        :return:
        """

        parent_columns = [c for c in self.original_column_names]
        aggs = []
        for child in self.children:
            aggs += child.to_table.get_aggregate_columns()

        for a in aggs:
            if a not in parent_columns:
                parent_columns.append(a)
        return parent_columns

    def get_aggregate_columns(self) -> List[Column]:
        """
        Get list of columns need to aggregate
        :return:
        """

        agg = []
        if self.parent and self.parent.parent:
            parent_columns = [c for c in self.parent.original_column_names]
            parent_parent_columns = [c for c in self.parent.parent.original_column_names]
            agg = self.get_aggregate_columns_util(parent_columns, self.original_column_names)
            agg += self.get_aggregate_columns_util(parent_parent_columns, self.original_column_names)

        elif self.parent and not self.parent.parent:
            parent_columns = [c for c in self.parent.original_column_names]
            self_columns = self.get_columns_after_aggregate()
            agg = self.get_aggregate_columns_util(parent_columns, self_columns)

        return agg

    def get_aggregate_columns_util(self, parent_columns: List[Column], self_columns: List[Column]) -> List[Column]:
        """
        Helper function. Return list of columns
        :param parent_columns:
        :param self_columns:
        :return:
        """
        agg = []
        for c in parent_columns:
            for cr in c.related_columns:
                if cr in self_columns:
                    agg.append(cr)
        return agg

    def has_column_with_name(self, column_name: str) -> bool:
        """
        table has the column with name
        :param column_name: Column name
        :return: True if has
        """
        for column in self.column_names:
            if column.equals_name(column_name):
                return True

        return False

    def has_column_with_name_without_aggregation(self, column_name: str) -> bool:
        """
        table has the column with name
        :param column_name: Column name
        :return: True if has
        """
        for column in self.original_column_names:
            if column.equals_name(column_name):
                return True

        return False

    def get_columns_used_in_select(self) -> List[Column]:
        columns_used_in_select = []
        for field in self.fields_used_in_select:
            for c in self.column_names:
                if c.equals_name(field):
                    columns_used_in_select.append(c)
        return columns_used_in_select

    def join(self, to_table: "Table", from_table_key: str, to_table_key: str):
        """
        Join another table. IF A join B, then A becomes the parent of B

        :param to_table_key: key from table_b.
        :param from_table_key: key from table_a, or self table.
        :param to_table: another table or table b.
        :return:
        """
        try:
            if not to_table.has_column_with_name(to_table_key):
                raise RuntimeError(f"Cannot find the key {to_table_key} in table {to_table}")

            if not self.has_column_with_name(from_table_key):
                raise RuntimeError(f"Cannot find the key {from_table_key} in table {self}")

            join_column = JoinColumn(to_table=to_table, to_table_key=to_table_key,
                                     from_table_key=from_table_key, from_table=self)
            self.children.append(join_column)
            to_table.parent = self
            to_column = join_column.to_table_join_column
            from_column = join_column.from_table_join_column

            to_column.related_columns.append(from_column)
            from_column.related_columns.append(to_column)
        except RecursionError:
            raise Exception(f"Join tree has a cycle. When joining {from_table_key} and {to_table_key}.")
        return self

    def get_root(self):
        """
        Return the root of the join tree
        :return:
        """
        if not self.parent:
            return self
        return self.parent.get_root()

    def to_json_graph(self, output_attrs: List[str], join_by=None):
        """
        Return a join graph in json format

        :param output_attrs:
        :param join_by:
        :return:
        """

        attrs = {}
        for column in self.original_column_names:
            attrs[column.name] = column.name

        return {
            "name": self.variable_table_name,
            "attributes": {"": f"{join_by if join_by else [f'{c.to_table_key} ' for c in self.children]}"},
            # "parent": self.parent.variable_table_name if self.parent else None,
            "children": [c.to_table.to_json_graph(output_attrs=output_attrs, join_by=c.to_table_key) for c in
                         self.children]
        }

    def to_json(self):
        return {
            "table_name": self.variable_table_name,
            "columns": [c.to_json() for c in self.original_column_names],
            "data_paths": self.data_paths,
            "data_sizes": self.data_sizes,
            "annotations": self.annotations
        }

    def clear_join(self):
        """
        Clear the join
        :return:
        """

        self.children = []
        self.parent = None

    def get_annotation_name(self, index=0):
        return f"{self.variable_table_name}_annotation_{index}"
