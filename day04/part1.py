from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    overlap = 0
    for line in lines:
        elf1, elf2 = line.split(',')
        elf1_min, elf1_max = elf1.split('-')
        elf2_min, elf2_max = elf2.split('-')

        elf1_min = int(elf1_min)
        elf1_max = int(elf1_max)
        elf2_min = int(elf2_min)
        elf2_max = int(elf2_max)

        if ((elf1_min >= elf2_min and elf1_max <= elf2_max)
                or (elf2_min >= elf1_min and elf2_max <= elf1_max)):
            overlap += 1

    # TODO: implement solution here!
    return overlap


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2


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
