import datetime
import tempfile
from textwrap import dedent

import pytest

from bookkeeper.utils import read_tree, date_converter


def test_create_tree():
    text = dedent('''
        parent1
            child1
                grandchild
            child2
        parent2
    ''')
    assert read_tree(text.splitlines()) == [
        ('parent1', None),
        ('child1', 'parent1'),
        ('grandchild', 'child1'),
        ('child2', 'parent1'),
        ('parent2', None)
    ]


def test_ignore_empty_strings():
    text = dedent('''
        parent1
            child1
                grandchild

            child2

        parent2
    ''')
    assert read_tree(text.splitlines()) == [
        ('parent1', None),
        ('child1', 'parent1'),
        ('grandchild', 'child1'),
        ('child2', 'parent1'),
        ('parent2', None)
    ]


def test_indentation_error():
    text = dedent('''
        parent1
            child1
                grandchild
          child2
    ''')
    with pytest.raises(IndentationError):
        read_tree(text.splitlines())


def test_with_file():
    text = dedent('''
        parent1
            child1
                grandchild
            child2
        parent2
    ''')
    with tempfile.TemporaryFile('w+') as f:
        f.write(text)
        f.seek(0)
        assert read_tree(f) == [
            ('parent1', None),
            ('child1', 'parent1'),
            ('grandchild', 'child1'),
            ('child2', 'parent1'),
            ('parent2', None)
        ]


def test_date_converter():
    date = datetime.datetime.now()
    res = date.strftime("%d.%m.%Y %H:%M")
    assert date_converter(date) == res
    assert date_converter(date.isoformat()) == res


def test_date_converter_error():
    with pytest.raises(ValueError):
        date_converter("11.11.1111")
