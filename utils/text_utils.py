import re
from collections import defaultdict
from itertools import combinations

from utils.common_utils import filter_and_format_pairs


class TextProcessor:
    def __init__(self, stopwords=None):
        """Initializes the text processor with optional stopwords."""
        self.stopwords = set(stopwords) if stopwords else set()

    def clean_text(self, text):
        """
        Cleans text by:
        - Lowercasing
        - Removing all punctuation (including hyphens)
        - Removing standalone and trailing hyphens
        - Filtering out stopwords
        """
        text = text.lower().strip()

        # Remove standalone and trailing hyphens
        text = re.sub(r'\b-\b', ' ', text)  # Standalone hyphens
        text = re.sub(r'(?<!\w)-|-(?!\w)', ' ', text)  # Hyphens at the start or end of words

        # Remove all non-alphanumeric characters except spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)

        words = text.split()
        cleaned_words = [word for word in words if word not in self.stopwords]  # Remove stopwords
        return " ".join(cleaned_words)

    def preprocess_sentences(self, sentences):
        """Cleans and tokenizes sentences, ensuring no empty lists are included."""
        return [self.clean_text(sentence).split() for sentence in sentences if self.clean_text(sentence).split()]

    def preprocess_people(self, people):
        """
        Cleans and processes names:
        - Keeps main names as a list of words.
        - Keeps nicknames as separate nested lists.
        - Removes stopwords from names and nicknames.
        """
        processed_people = []
        for person in people:
            main_name_parts = [word for word in self.clean_text(person[0]).split() if word not in self.stopwords]
            nicknames = [[word for word in self.clean_text(nick).split() if word not in self.stopwords]
                         for nick in person[1].split(',')] if len(person) > 1 and person[1].strip() else []
            processed_people.append([main_name_parts, nicknames])
        return processed_people


def count_person_mentions(sentences, people):
    """
    Counts the number of times each person's name (including nicknames) appears in the text.
    - Matches full names.
    - Matches hyphenated words correctly.
    - Matches each individual word in a name separately.
    - Filters out names with 0 mentions.
    """
    mention_counts = defaultdict(int)

    # Create a mapping of name variations → main name
    name_mapping = {variation: " ".join(person[0]) for person in people for variation in
                    [" ".join(person[0])] + [" ".join(nick) for nick in person[1]]}

    # Initialize mention counts for each main name
    for main_name in set(name_mapping.values()):
        mention_counts[main_name] = 0

    # Count occurrences of names in sentences
    for sentence in sentences:
        sentence_str = " ".join(sentence)  # Convert to a single string

        for name_variant, main_name in name_mapping.items():
            # Match full names exactly
            full_name_matches = re.findall(r'\b' + re.escape(name_variant) + r'\b', sentence_str)
            mention_counts[main_name] += len(full_name_matches)

            # Match individual words in multi-word names
            for word in name_variant.split():
                word_matches = re.findall(r'\b' + re.escape(word) + r'\b', sentence_str)
                mention_counts[main_name] += len(word_matches)

    # Remove names with 0 mentions and return sorted results
    return sorted((name, count) for name, count in mention_counts.items() if count > 0)


def preprocess_k_seq_lookup(sentences, max_k):
    """
    Preprocesses sentences into a hash table for O(1) lookup of K-sequences.

    Parameters:
        sentences (list of lists): Preprocessed sentences.
        max_k (int): Maximum K value for sequences.

    Returns:
        dict: A dictionary mapping each K-sequence to the list of sentences containing it.
    """
    k_seq_lookup = defaultdict(list)

    for sentence in sentences:
        sentence_str = " ".join(sentence)  # Convert sentence list to string
        for k in range(1, max_k + 1):  # Generate sequences for all k up to max_k
            for i in range(len(sentence) - k + 1):
                k_seq = " ".join(sentence[i:i + k])
                k_seq_lookup[k_seq].append(sentence_str)  # Store sentence in hashmap

    return k_seq_lookup


def extract_k_seqs(sentence, max_k):
    """
    Extracts all k-sequences (subsequences of length 1 to max_k) from a given sentence.

    :param sentence: List of words in a sentence.
    :param max_k: Maximum length of sequences to extract.
    :return: List of extracted k-sequences as strings.
    """
    k_seqs = []
    for k in range(1, max_k + 1):  # Extract sequences of lengths 1 to max_k
        for i in range(len(sentence) - k + 1):
            k_seq = " ".join(sentence[i:i + k])  # Create k-seq string
            k_seqs.append(k_seq)
    return k_seqs


def get_valid_pairs(sentences, people, windowsize, threshold):
    # Map people to sentences
    sentence_people = map_people_to_sentences(sentences, people)

    # Compute co-occurrences within sliding windows
    co_occurrences = compute_co_occurrences(sentence_people, windowsize)

    # Filter by threshold and format output
    return filter_and_format_pairs(co_occurrences, people, threshold)


def map_people_to_sentences(sentences, people):
    """
    Maps each sentence to the set of people appearing in it.

    :param sentences: List of tokenized sentences.
    :param people: List of processed people names.
    :return: List of sets, where each set contains the names found in that sentence.
    """
    all_names, name_variations = build_name_lookup(people)
    return extract_people_from_sentences(sentences, all_names, name_variations)


def extract_people_from_sentences(sentences, all_names, name_variations):
    """
    Extracts people mentions from sentences based on a prebuilt name lookup.

    :param sentences: List of tokenized sentences.
    :param all_names: Set of all known names and variations.
    :param name_variations: Dictionary mapping variations to full names.
    :return: List of sets where each set contains detected names for a sentence.
    """
    sentence_people = [set() for _ in sentences]

    for i, sentence in enumerate(sentences):
        for word in sentence:
            if word in all_names:  # If the word is a known name
                matched_names = set()  # Collect all possible full names

                # Retrieve all names containing this word
                for name in all_names:
                    if word in name.split():  # Match partial words inside full names
                        matched_names.add(name)

                # Ensure the exact name itself is included
                if word in name_variations:
                    matched_names.add(word)

                # Add all matches to the sentence
                sentence_people[i].update(matched_names)

    return sentence_people


def find_all_matching_names(word, all_names, name_variations):
    """
    Finds all full names that contain the given word.

    :param word: A word detected in the sentence.
    :param all_names: A set of all known names.
    :param name_variations: A dictionary mapping name variations to full names.
    :return: A set of all full names that include the word.
    """
    matched_names = set()

    for name in all_names:
        if word in name.split():  # Ensure partial name matches
            matched_names.add(name_variations.get(name, name))  # Map to full name if exists

    return matched_names


def build_name_lookup(people):
    """
    Builds a lookup set of all name variations and a mapping of each variation to the main name.
    Debugs name mapping structure.
    """
    all_names = set()
    name_variations = {}  # {name_variant: main_name}

    for person_variants in people:
        main_name = " ".join(person_variants[0])
        all_names.add(main_name)
        # Include parts of the main name
        for name in person_variants[0]:
            all_names.add(name)
            name_variations[name] = main_name
        # Include full nicknames (fixing single words to full strings)
        if len(person_variants) > 1 and person_variants[1]:
            for nickname in person_variants[1]:
                nickname_str = " ".join(nickname)
                all_names.add(nickname_str)
                name_variations[nickname_str] = main_name
    return all_names, name_variations


def compute_co_occurrences(sentence_people, window_size):
    """
    Computes the number of windows where each pair of names co-occur.
    Debugs window detection and pair counting.
    """
    co_occurrence_counts = defaultdict(int)

    for i in range(len(sentence_people) - window_size + 1):
        window = set()
        for j in range(window_size):
            window.update(sentence_people[i + j])

        for person1, person2 in combinations(sorted(window), 2):
            co_occurrence_counts[(person1, person2)] += 1

    return co_occurrence_counts
