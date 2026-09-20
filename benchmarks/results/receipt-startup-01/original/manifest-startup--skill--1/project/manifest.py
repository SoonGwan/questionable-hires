import builtins
import csv

def parse_record(record):
    return next(csv.reader([record], delimiter=builtins.MANIFEST_DELIMITER, strict=True))
