from utils.common_utils import Formatter
from utils.file_utils import load_json, load_pair_from_file
from tasks.task_7 import build_graph

def find_fixed_length_path(graph, start, end, fixed_length):
    def dfs(current, path, length):
        if length == fixed_length:
            return current == end

        if length > fixed_length:
            return False

        for neighbor in graph.get(current, []):
            if neighbor not in path:
                if dfs(neighbor, path + [neighbor], length + 1):
                    return True

        return False

    return dfs(start, [start], 0)

def check_pairs_in_clusters(pairs, person_to_cluster):
    results = []
    for name1, name2 in pairs:
        clusters1 = set(person_to_cluster.get(name1, []))
        clusters2 = set(person_to_cluster.get(name2, []))
        in_same_cluster = bool(clusters1 & clusters2)  # Check for any overlap
        results.append([name1, name2, in_same_cluster])
    return results

def task_8(args):
    """
    Executes Task 8: Identifies clusters and checks if name pairs belong to the same cluster.
    """
    # Load pairs from file or Task 6 results
    co_occurrence_pairs = load_pair_from_file(args)

    # Build graph from valid co-occurrence pairs
    graph = build_graph(co_occurrence_pairs)

    # Load the pairs we need to check
    people_connections = load_json(args.pairs)["keys"]

    # Check which pairs belong to the same cluster
    pair_matches = [
        [name1, name2, find_fixed_length_path(graph, name1, name2, args.fixed_length)]
        for name1, name2 in people_connections
    ]

    # Print formatted output
    print(Formatter.format_task_8_output(pair_matches))