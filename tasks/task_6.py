from utils.file_utils import load_basic_args, load_json
from utils.text_utils import get_valid_pairs


def task_6(args):
    """
    Executes Task 6: Identifies co-occurring people in text within a sliding window.
    """
    # Load and preprocess data
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        sentences = data["Question 1"]["Processed Sentences"]
        people = data["Question 1"]["Processed Names"]
    else:
        sentences, people = load_basic_args(args)
    #find valid_pairs
    valid_pairs = get_valid_pairs(sentences, people, args.windowsize, args.threshold)
    print(valid_pairs)
