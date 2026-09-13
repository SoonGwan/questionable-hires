def order(graph):
    visited = set()
    output = []
    active = set()
    def visit(node):
        if node in visited:
            return
        if node in active:
            raise ValueError("cyclic dependency")
        active.add(node)
        for dependency in graph[node]:
            visit(dependency)
        active.remove(node)
        visited.add(node)
        output.append(node)
    for node in graph:
        visit(node)
    return output
