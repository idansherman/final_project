import csv
import os
import sys
import json

from utils.text_utils import TextProcessor, get_valid_pairs

TASK_REQUIREMENTS = {
    1: ["names"],
    2: ["maxk"],
    3: [],
    4: ["qsek_query_path"],
    5: ["maxk"],
    6: ["windowsize", "threshold"],
    7: ["pairs", "maximal_distance"],
    8: ["pairs", "fixed_length"]
}
# Define which task parameters are integers (to avoid treating them as files)
INTEGER_PARAMS = {
    "maxk": (1, float("inf")),  # Must be at least 1
    "windowsize": (0, float("inf")),
    "threshold": (0, float("inf")),
    "maximal_distance": (0, float("inf")),
    "fixed_length": (0, float("inf")),
}


def load_csv(file_path, as_list=True):
    """Reads a CSV file and returns its content as a list of rows."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                if as_list:
                    data.append(row)  # Keeps full rows (Task 1)
                else:
                    data.append(row[0] if len(row) > 0 else "")
    return data


def load_stopwords(file_path):
    """Loads stopwords from a CSV file into a set."""
    stopwords = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                stopwords.add(row[0].strip().lower())
    return stopwords

def load_basic_args(args):
    stopwords = load_stopwords(args.removewords)
    text_processor = TextProcessor(stopwords)
    sentences = text_processor.preprocess_sentences(load_csv(args.sentences, False))
    people = text_processor.preprocess_people(load_csv(args.names))
    return sentences, people

def load_json(file_path):
    """Loads a JSON file and returns its contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(file_path):
    """Checks if a file exists, is not empty, and contains at least one valid row."""
    if not file_path or not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if any(cell.strip() for cell in row):  # Ensure at least one cell is non-empty
                return True
    return False  # If all rows are empty, return False


def validate_input(args, tasks):
    """Validates required arguments and files before running a task."""

    # Check if the task is valid
    if args.task not in tasks:
        print(f"Task {args.task} is not available.", file=sys.stderr)
        sys.exit(1)

    task_params = TASK_REQUIREMENTS.get(args.task, [])
    required_values = []

    # Handle preprocessed files
    if args.preprocessed and args.task != 1:
        if not os.path.exists(args.preprocessed[0]):
            print(f"Invalid input: Preprocessed file `{args.preprocessed[0]}` does not exist.", file=sys.stderr)
            sys.exit(1)
        # Use the preprocessed file instead of separate files
        required_files = [args.preprocessed[0]]
    else:
        # If no preprocessed file, collect missing required files
        required_files = [args.sentences, args.removewords]

        # Additional required files based on the task
        if args.task in {3, 5, 6}:
            required_files.append(args.names)
        elif args.task in {7, 8}:
            required_files.append(args.names)
            required_values = ["windowsize", "threshold"]


        # Collect all required parameters (from TASK_REQUIREMENTS)

        # Separate file-based parameters and integer parameters
    required_files += [getattr(args, param, None) for param in task_params if param not in INTEGER_PARAMS]
    required_values += [param for param in task_params if param in INTEGER_PARAMS]

    # Validate file existence
    required_files = [f for f in required_files if isinstance(f, str)]  # Ensure only valid paths
    missing_files = [f for f in required_files if f and not os.path.exists(f)]
    if missing_files:
        print(f"Invalid input: The following required files are missing or incorrect:\n{missing_files}", file=sys.stderr)
        sys.exit(1)

    # Validate integer parameters
    for param in required_values:
        value = getattr(args, param, None)
        min_val = 1 if param == "maxk" else 0  # maxk must be ≥ 1, others can be 0+
        if value is None or not isinstance(value, int) or value < min_val:
            print(f"Invalid input: `{param}` must be an integer ≥ {min_val}.", file=sys.stderr)
            sys.exit(1)

def load_pair_from_file(args):
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        co_occurrence_pairs = data["Question 6"]["Pair Matches"]
    else:
        sentences, people = load_basic_args(args)
        co_occurrence_pairs = get_valid_pairs(sentences, people, args.windowsize, args.threshold)

    return co_occurrence_pairs
