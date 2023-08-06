from typing import Tuple, List, Optional

from sqlparse.sql import Where, Comparison

from codegen.codegen import Parser
from codegen.node.cpp_nodes.WhereNode import FreeConnexWhereNode
from codegen.table import Table, FreeConnexTable


class FreeConnexParser(Parser):
    """
    Construct a Free Connex SQL Query parser.
    This will try to construct a free connex join tree instead of the regular join tree
    which the base class "Parser" will generate by default.
    """

    def is_free_connex(self) -> Tuple[bool, List["Table"]]:
        """
        Check whether the current join tree is a free connex join tree.

        :return: a tuple. The first item in the tuple indicates whether the join tree is a free connex join tree.

        The second argument in the tuple indicates a list of tables which cause the problem
        if the tree is not a free connex join tree
        """

        root_table: Optional[FreeConnexTable] = self.root_table
        height = root_table.get_height()
        output_attrs = self.get_output_attributes()
        non_output_attrs = self.get_non_output_attributes(output_attrs=output_attrs)
        is_valid = self.check_valid(raise_error=False)

        is_free_connex, tables = root_table.is_free_connex(output_attrs=output_attrs,
                                                           non_output_attrs=non_output_attrs,
                                                           height=height)

        return is_free_connex and is_valid, tables

    def __parse_where__(self, token: Where):
        last = self.root.get_last_node()
        comparison_list: List[Comparison] = []
        for t in token.tokens:
            if type(t) == Comparison:
                comparison_list.append(t)
        last.next = FreeConnexWhereNode(comparison_list=comparison_list, tables=self.tables,
                                        is_free_connex_table=self.is_free_connex)
        last.next.prev = last
