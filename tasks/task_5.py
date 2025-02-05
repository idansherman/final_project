import json
from collections import defaultdict
from utils.file_utils import load_csv, load_json, load_stopwords, load_basic_args
from utils.text_utils import TextProcessor
from utils.common_utils import Formatter


def extract_contexts(sentences, people, k):
    """
    Extracts k-sequence contexts for each person mentioned in the sentences.
    Uses efficient indexing and k-sequence extraction.

    :param sentences: List of tokenized sentences.
    :param people: List of processed people names.
    :param k: Maximum number of words in the sequence.
    :return: Dictionary mapping person names to their k-sequences.
    """

    person_contexts = defaultdict(set)  # Dictionary to store results

    # Step 1: Build a lookup dictionary for fast sentence retrieval
    word_to_sentences = defaultdict(set)
    for idx, sentence in enumerate(sentences):
        for word in set(sentence):  # Avoid duplicate entries for the same sentence
            word_to_sentences[word].add(idx)

    # Step 2: Extract Contexts Using Name Variants
    for person_variants in people:
        main_name = " ".join(person_variants[0])  # Full name as a single string
        name_variants = {main_name}  # Start with the full name

        # Add each individual word from the main name
        name_variants.update(person_variants[0])  # Adds words like "harry" and "potter"

        # Add full nicknames (do NOT break them apart)
        name_variants.update(" ".join(nick) for nick in person_variants[1])

        matched_sentences = set()
        for name in name_variants:
            for word in name.split():  # Allow partial name matches
                if word in word_to_sentences:
                    matched_sentences.update(word_to_sentences[word])  # Ensure we collect all relevant sentences

        # Extract k-sequence contexts
        for sentence_idx in matched_sentences:
            sentence = sentences[sentence_idx]
            for i in range(len(sentence)):
                if any(name_variant in " ".join(sentence) for name_variant in name_variants):
                    # Generate k-word sequences up to max_k
                    for seq_len in range(1, k + 1):  # Ensure we do not exceed max_k
                        if i + seq_len <= len(sentence):
                            context = " ".join(sentence[i : i + seq_len])
                            person_contexts[main_name].add(context)  # Store in set to avoid duplicates

    # Step 3: Convert Sets to Sorted Lists & Ensure Empty Names Are Removed
    formatted_output = {
        person: sorted(person_contexts[person])  # Sort sequences alphabetically
        for person in sorted(person_contexts.keys())  # Sort names lexicographically
        if person_contexts[person]  # Ensure we remove empty names
    }

    return formatted_output


def task_5(args):
    """
    Executes Task 5: Extracting K-sequence contexts for named entities.
    """

    # Load and preprocess data
    if args.preprocessed:
        data = load_json(args.preprocessed[0])
        sentences = data["Question 1"]["Processed Sentences"]
        people = data["Question 1"]["Processed Names"]
    else:
        sentences, people = load_basic_args(args)

    max_k = args.maxk  # The k-sequence length

    # Extract k-sequence contexts
    person_contexts = extract_contexts(sentences, people, max_k)

    # Format and print output
    formatted_output = Formatter.format_task_5_output(person_contexts)
    print(formatted_output)