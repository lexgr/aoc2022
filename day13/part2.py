from __future__ import annotations

import argparse
import ast
import enum
import functools
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Result = enum.Enum('Result', 'EQ GOOD BAD')

ListLike = int | list['ListLike']


def compare(lhs: ListLike, rhs: ListLike) -> Result:
    if isinstance(lhs, int) and not isinstance(rhs, int):
        lhs = [lhs]
    elif not isinstance(lhs, int) and isinstance(rhs, int):
        rhs = [rhs]

    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs < rhs:
            return Result.GOOD
        elif lhs == rhs:
            return Result.EQ
        else:
            return Result.BAD
    elif isinstance(lhs, list) and isinstance(rhs, list):
        for a, b in itertools.zip_longest(lhs, rhs):
            if a is None:
                return Result.GOOD
            elif b is None:
                return Result.BAD

            compared = compare(a, b)
            if compared is not Result.EQ:
                return compared

        return Result.EQ
    else:
        raise AssertionError('unreachable')


def compute(s: str) -> int:
    s = s.replace('\n\n', '\n')
    lists = [ast.literal_eval(line) for line in s.splitlines()]

    def implements_cmp(l1: ListLike, l2: ListLike) -> int:
        ret = compare(l1, l2)
        if ret == Result.EQ:
            return 0
        elif ret == Result.GOOD:
            return -1
        else:
            return 1

    lists.extend(([[2]], [[6]]))
    lists.sort(key=functools.cmp_to_key(implements_cmp))

    idx1 = lists.index([[2]])
    idx2 = lists.index([[6]])
    return (idx1 + 1) * (idx2 + 1)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
