#!/usr/bin/env python3

import argparse
import sys
from utils.file_utils import validate_input
from tasks.task_1 import task_1
from tasks.task_2 import task_2
from tasks.task_3 import task_3
from tasks.task_4 import task_4
from tasks.task_5 import task_5
from tasks.task_6 import task_6
from tasks.task_7 import task_7
from tasks.task_8 import task_8

TASKS = {1: task_1, 2: task_2, 3: task_3, 4: task_4,
         5: task_5, 6: task_6, 7: task_7, 8: task_8}


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True,
                        type=int
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )
    return parser.parse_args(args)


def main():
    args = readargs()
    validate_input(args, TASKS)

    if args.task in TASKS:
        TASKS[args.task](args)  # Calls the correct task function dynamically
    else:
        print(f"Task {args.task} is not available.")
        sys.exit(1)


if __name__ == "__main__":
    main()
