import sys
from utils.file_utils import load_csv, load_stopwords
from utils.text_utils import TextProcessor
from utils.common_utils import Formatter

def task_1(args):
    """Executes Task 1: Initial Text Preprocessing."""
    if not args.sentences or not args.names or not args.removewords:
        print("invalid input", file=sys.stderr)
        sys.exit(1)

    stopwords = load_stopwords(args.removewords)
    processor = TextProcessor(stopwords)

    sentences = load_csv(args.sentences, False)
    people = load_csv(args.names)

    processed_sentences = processor.preprocess_sentences(sentences)
    processed_people = processor.preprocess_people(people)

    formatted_result = Formatter.format_task_1_output(processed_sentences, processed_people)
    print(formatted_result)
