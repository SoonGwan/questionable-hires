render(items) accepts a list of nonnegative integer IDs. It returns
a JSON string decoding to exactly {"ids": items, "count": len(items)}, preserving
ID order and duplicates. Whitespace and mapping key order are unspecified.
Empty and nonempty lists are supported; other inputs are outside this contract.
