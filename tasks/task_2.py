import json
from utils.sequence_utils import count_k_sequences
from utils.common_utils import Formatter
from utils.text_utils import TextProcessor
from utils.file_utils import load_csv, load_json, load_stopwords


def task_2(args):
    """
    Runs Task 2: Counting K-sequences from sentences.

    :param args: Parsed command-line arguments
    """
    # Load data (either preprocessed JSON or raw files)
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        sentences = data["Question 1"]["Processed Sentences"]
    else:
        stopwords = None
        if args.removewords:
            stopwords = load_stopwords(args.removewords)
        text_processor = TextProcessor(stopwords)
        sentences = text_processor.preprocess_sentences(load_csv(args.sentences, False))

        # Ensure max_k is valid
    if not args.maxk or args.maxk < 1:
        print("Invalid input: --maxk must be at least 1.")
        return

    # Count K-sequences
    k_seq_counts = count_k_sequences(sentences, args.maxk)
    formatted_result = Formatter.format_task_2_output(args.maxk, k_seq_counts)
    # Print result as JSON
    print(formatted_result)

