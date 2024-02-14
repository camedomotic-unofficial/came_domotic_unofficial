# Gets from the JSON response all the items with "leaf": true
def find_leaf_nodes(node):
    """
    Recursive function that finds all the "leaf" nodes
    in a nested dictionary or list.

    :param node: the node to search
    :return: a generator with the leaf nodes
    """
    if isinstance(node, dict):
        if node.get("leaf") is True:
            yield node
        else:
            for child in node.values():
                yield from find_leaf_nodes(child)
    elif isinstance(node, list):
        for child in node:
            yield from find_leaf_nodes(child)
