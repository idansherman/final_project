import json
from collections import deque, defaultdict


def build_graph(task6_output):
    """
    Constructs an adjacency list graph from Task 6 output.

    :param task6_output: JSON string returned from Task 6.
    :return: Dictionary representing the adjacency list of the graph.
    """
    graph = defaultdict(set)

    # Load JSON if it's a string
    if isinstance(task6_output, str):
        task6_output = json.loads(task6_output)

    # Extract "Pair Matches"
    pair_matches = task6_output.get("Question 6", {}).get("Pair Matches", [])

    for pair in pair_matches:
        if len(pair) != 2:
            continue  # Skip malformed pairs

        # Flatten each person's name into a single string
        name1 = " ".join(pair[0])
        name2 = " ".join(pair[1])

        # Add to graph as an undirected edge
        graph[name1].add(name2)
        graph[name2].add(name1)

    return graph


def shortest_path_by_bfs(graph, start, end, max_distance):
    """
    Uses Breadth-First Search (BFS) to find the shortest path between two names.

    :param graph: The adjacency list of name co-occurrences.
    :param start: The starting person's name.
    :param end: The target person's name.
    :param max_distance: Maximum allowed distance for a valid connection.
    :return: True if path length is <= max_distance, False otherwise.
    """
    if start == end:
        return True  # Trivial case: same person

    queue = deque([(start, 0)])  # (current_node, current_distance)
    visited = {start}

    while queue:
        node, distance = queue.popleft()

        if distance > max_distance:
            break  # Stop if exceeding max allowed jumps

        for neighbor in graph.get(node, []):
            if neighbor == end:
                return True  # Found a valid path
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return False  # No path within max_distance