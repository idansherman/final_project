import json

from utils.common_utils import Formatter
from utils.file_utils import load_csv, load_stopwords, load_basic_args, load_json
from utils.text_utils import TextProcessor, count_person_mentions


def task_3(args):
    """
    Executes Task 3: Counting Person Mentions.
    """
    # Load and preprocess data
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        sentences = data["Question 1"]["Processed Sentences"]
        people = data["Question 1"]["Processed Names"]
    else:
        sentences, people = load_basic_args(args)

    # Counts person mentions
    name_mentions = count_person_mentions(sentences, people)

    print(Formatter.format_task_3_output(name_mentions))