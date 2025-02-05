from utils.file_utils import load_json, load_basic_args, load_pair_from_file
from utils.common_utils import Formatter
from utils.graph_utils import build_graph, shortest_path_by_bfs
from utils.text_utils import get_valid_pairs


def task_7(args):
    """
    Handles Task 7: Determines if name pairs are within a given max_distance in the co-occurrence graph.

    :param args: CLI arguments containing file paths and max_distance.
    """
    # Load or generate co-occurrence data
    pair_matches = load_pair_from_file(args)

    # Build the graph from co-occurrences
    graph = build_graph(pair_matches)
    # Read name pairs from People_connections file
    people_connections = load_json(args.pairs)

    # Determine shortest path relationships
    results = []
    for name1, name2 in people_connections["keys"]:
        is_connected = shortest_path_by_bfs(graph, name1, name2, args.maximal_distance)
        results.append([name1, name2, is_connected])
    # Format and print output
    print(Formatter.format_task_7_output(results))
