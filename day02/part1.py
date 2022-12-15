from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

scores = {'X': 1, 'Y': 2, 'Z': 3}
win = {'X': 'C', 'Y': 'A', 'Z': 'B'}

mapping_them = {'A': 'R', 'B': 'P', 'C': 'S'}
mapping_you = {'X': 'R', 'Y': 'P', 'Z': 'S'}


def compute(s: str) -> int:
    lines = s.splitlines()
    score = 0
    for line in lines:
        they, you = line.split()
        score += scores[you]
        if they == win[you]:
            score += 6
        elif mapping_them[they] == mapping_you[you]:
            score += 3
    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
