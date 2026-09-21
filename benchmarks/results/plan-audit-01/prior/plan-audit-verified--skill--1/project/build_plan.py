def plan(dependencies):
    remaining = {name: set(parents) for name, parents in dependencies.items()}
    ready = [name for name, parents in remaining.items() if not parents]
    order = []
    while ready:
        name = ready.pop(0)
        order.append(name)
        del remaining[name]
        for child, parents in remaining.items():
            parents.discard(name)
            if not parents and child not in ready:
                ready.append(child)
    if remaining:
        raise ValueError("dependency cycle")
    return order
