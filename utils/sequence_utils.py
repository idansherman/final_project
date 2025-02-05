from collections import defaultdict


def count_k_sequences(sentences, max_k):
    """
    Extracts k-sequences from the given sentences and counts occurrences.

    - Ensures correct counting across all sentences.
    - No unnecessary duplicate blocking.
    """
    k_seq_counts = {k: defaultdict(int) for k in range(1, max_k + 1)}

    for sentence in sentences:
        for k in range(1, max_k + 1):
            for i in range(len(sentence) - k + 1):
                k_seq = " ".join(sentence[i: i + k])
                k_seq_counts[k][k_seq] += 1

    return {k: dict(v) for k, v in k_seq_counts.items()}
