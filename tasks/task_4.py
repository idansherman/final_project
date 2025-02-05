import json

from utils.common_utils import Formatter
from utils.file_utils import load_csv, load_json, load_stopwords
from utils.text_utils import TextProcessor


def task_4(args):
    """
    Executes Task 4: Searching for K-seq Matches in Sentences.
    """
    # Load and preprocess data
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        sentences = data["Question 1"]["Processed Sentences"]
    else:
        stopwords = load_stopwords(args.removewords)
        text_processor = TextProcessor(stopwords)
        sentences = text_processor.preprocess_sentences(load_csv(args.sentences, False))

    # Load k-seq queries
    # Ensure unique k-seq queries while preserving order
    seen = set()
    k_seq_queries = []
    for k_seq in load_json(args.qsek_query_path)["keys"]:
        k_seq_tuple = tuple(k_seq)
        if k_seq_tuple not in seen:
            seen.add(k_seq_tuple)
            k_seq_queries.append(k_seq_tuple)  # Keep it as a tuple for consistent structure

    # Build index for fast lookup (convert sentences to sets of words for quick matching)
    sentence_index = {tuple(sentence): sentence for sentence in sentences}

    # Find matches
    k_seq_matches = []
    for k_seq in k_seq_queries:
        k_seq_str = " ".join(k_seq)  # Convert k-seq to string for matching
        matching_sentences = [
            sentence_index[sent] for sent in sentence_index if all(word in sent for word in k_seq)
        ]

        if matching_sentences:  # ✅ Only add if there are matches
            k_seq_matches.append([k_seq_str, matching_sentences])

    # **Sorting for consistency**
    k_seq_matches.sort(key=lambda x: x[0])  # Sort by k-seq string

    for match in k_seq_matches:
        match[1].sort()  # Ensure sentences are sorted

    # Format and print output
    formatted_output = Formatter.format_task_4_output(k_seq_matches)
    print(formatted_output)