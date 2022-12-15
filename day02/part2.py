from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

scores = {'R': 1, 'P': 2, 'S': 3}
win = {'X': 'C', 'Y': 'A', 'Z': 'B'}

mapping_them = {'A': 'R', 'B': 'P', 'C': 'S'}
mapping_win = {'A': 'P', 'B': 'S', 'C': 'R'}
mapping_lose = {'A': 'S', 'B': 'R', 'C': 'P'}
what_to_do = {'X': 'lose', 'Y': 'draw', 'Z': 'win'}


def compute(s: str) -> int:
    lines = s.splitlines()
    score = 0
    for line in lines:
        they, you = line.split()
        if what_to_do[you] == 'win':
            score += 6
            score += scores[mapping_win[they]]
        elif what_to_do[you] == 'draw':
            score += 3
            score += scores[mapping_them[they]]
        else:
            score += scores[mapping_lose[they]]

    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
