"""
Utility functions
"""


from typing import Iterable, Generator


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _lines_with_indent(lines: Iterable[str]) -> Generator[tuple[int, str], None, None]:
    for line in lines:
        if not line or line.isspace():
            continue
        yield _get_indent(line), line.strip()


def read_tree(lines: Iterable[str]) -> list[tuple[str, str | None]]:
    """
    Read tree structure from indented text file. Return pairs of child-parent.
    Root's parent is None

    Example. The following text:
    parent
        child1
            child2
        child3

    will give the tree: [('parent', None), ('child1', 'parent'), ('child2', 'child1'), ('child3', 'parent')]

    Empty lines are ignored.

    Parameters
    ----------
    lines - Iterable of lines (file object or list of lines)

    Returns
    -------
    List of child-parent pairs

    """
    parents: list[tuple[str | None, int]] = []
    last_indent = -1
    last_name = None
    result: list[tuple[str, str | None]] = []
    for i, (indent, name) in enumerate(_lines_with_indent(lines)):
        if indent > last_indent:
            parents.append((last_name, last_indent))
        elif indent < last_indent:
            while indent < last_indent:
                _, last_indent = parents.pop()
            if indent != last_indent:
                raise IndentationError(
                    f'unindent does not match any outer indentation '
                    f'level in line {i}:\n'
                )
        result.append((name, parents[-1][0]))
        last_name = name
        last_indent = indent
    return result
