from copy import deepcopy


def dispatch(payload, handlers):
    results = []
    for handler in handlers:
        try:
            results.append(handler(deepcopy(payload)))
        except ValueError as error:
            raise ValueError(str(error)) from error
    return results
