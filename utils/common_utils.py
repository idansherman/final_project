import json


class Formatter:

    @staticmethod
    def format_output(task_number, data):
        """
        Generic formatter for any task output.
        :param task_number: Task number (int)
        :param data: Data to format
        :return: JSON formatted string without unnecessary \n escapes
        """
        return json.dumps({f"Question {task_number}": data}, indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_1_output(processed_sentences, processed_names):
        """
        Formats output for Task 1.
        """
        return Formatter.format_output(1, {
            "Processed Sentences": processed_sentences,
            "Processed Names": processed_names
        })

    @staticmethod
    def format_task_2_output(max_k, k_seq_counts):
        """
        Formats the output for Task 2.
        """
        formatted_k_seq_counts = []

        for k in range(1, max_k + 1):
            key = f"{k}_seq"
            sequences = k_seq_counts.get(k, {})
            sorted_sequences = [[seq, count] for seq, count in sorted(sequences.items(), key=lambda x: x[0])]
            formatted_k_seq_counts.append([key, sorted_sequences])

        return json.dumps({
            "Question 2": {
                f"{max_k}-Seq Counts": formatted_k_seq_counts
            }
        }, indent=4, ensure_ascii=False)

    @staticmethod
    def format_task_3_output(name_mentions):
        """
        Formats the output for Task 3 (Name Mentions).
        """
        sorted_mentions = sorted(name_mentions, key=lambda x: x[0])  # Sort names lexicographically
        return json.dumps({
            "Question 3": {
                "Name Mentions": sorted_mentions
            }
        }, indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_4_output(k_seq_matches):
        """
        Formats the output for Task 4 (K-Seq Matches).
        """
        # Ensure K-Seq Matches are sorted by sequence name
        sorted_matches = sorted(k_seq_matches, key=lambda x: x[0])
        for match in sorted_matches:
            match[1].sort()

        return json.dumps({
            "Question 4": {
                "K-Seq Matches": sorted_matches
            }
        }, indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_5_output(person_contexts):
        """
        Formats the output for Task 5: Ensures proper structure, sorting, and removal of empty entries.

        :param person_contexts: Dictionary mapping person names to their k-sequence lists.
        :return: JSON formatted string with the correct structure (list format).
        """
        formatted_output = []

        # Sort names lexicographically
        sorted_people = sorted(person_contexts.keys())

        for person in sorted_people:
            k_sequences = sorted(set(person_contexts[person]))  # Unique & sorted

            # ✅ Convert each k-sequence from a string to a list of words
            k_sequences = [seq.split() for seq in k_sequences]

            if k_sequences:  # ✅ Only include names with actual k-sequences
                formatted_output.append([person, k_sequences])

        # If no valid results, return an empty list `[]`
        return json.dumps({"Question 5": {"Person Contexts and K-Seqs": formatted_output}},
                          indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_6_output(valid_pairs):
        """
        Formats the output for Task 6.

        :param valid_pairs: List of valid name pairs.
        :return: Formatted JSON string.
        """
        return json.dumps({"Question 6": {"Pair Matches": valid_pairs}}, indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_7_output(pair_matches):
        """
        Formats and sorts the output for Task 7.

        :param pair_matches: List of pairs with boolean values.
        :return: Properly formatted JSON output with sorted order.
        """
        # Ensure each pair is sorted alphabetically within itself
        sorted_pairs = [[sorted(pair[:2])[0], sorted(pair[:2])[1], pair[2]] for pair in pair_matches]

        # Ensure the full list is sorted by the **first name in each pair**, then by the second
        sorted_pairs.sort(key=lambda x: (x[0], x[1]))

        return json.dumps({"Question 7": {"Pair Matches": sorted_pairs}}, indent=2, ensure_ascii=False)

    @staticmethod
    def format_task_8_output(pair_matches):
        """
        Formats output for Task 8.

        :param pair_matches: List of name pairs with boolean values indicating if they are in the same cluster.
        :return: JSON formatted string.
        """

        # Ensure each pair is sorted alphabetically within itself
        sorted_pairs = [[sorted(pair[:2])[0], sorted(pair[:2])[1], pair[2]] for pair in pair_matches]

        # Ensure the full list is sorted by the **first name in each pair**, then by the second
        sorted_pairs.sort(key=lambda x: (x[0], x[1]))

        return json.dumps({"Question 8": {"Pair Matches": sorted_pairs}}, indent=2, ensure_ascii=False)


def filter_and_format_pairs(co_occurrence_counts, people, threshold):
    """
    Filters valid co-occurrence pairs based on the threshold and ensures both names exist in the dataset.

    :param co_occurrence_counts: Dictionary {(name1, name2): count} storing co-occurrence counts.
    :param people: List of processed full names (ensuring validity of names in pairs).
    :param threshold: Minimum number of occurrences required for a valid pair.
    :return: List of valid pairs formatted correctly.
    """
    valid_pairs = []
    full_names_set = set(" ".join(person[0]) for person in people)  # Convert list format to full names

    for (name1, name2), count in co_occurrence_counts.items():
        if count >= threshold:
            # Ensure both names exist in full names list before adding
            if name1 in full_names_set and name2 in full_names_set:
                valid_pairs.append([name1.split(), name2.split()])

    sorted(valid_pairs)
    return Formatter.format_task_6_output(valid_pairs)

