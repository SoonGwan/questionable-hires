I’ll read `labels.py` and explain the result, whitespace handling, and ordering.

`labels(['  Ada ', '', 'Lin'])` returns:

```python
['ADA', 'LIN']
```

It removes leading and trailing whitespace and converts each retained name to uppercase. Empty strings and whitespace-only strings are excluded. Internal whitespace is preserved.

The function preserves the input order of retained names; it does not sort them.
