# Catalog working rules

Retain QA tests only under qa/, named test_*.py. Import the actual search implementation; do not copy its logic into a test. Verify empty-query results as the normal sequence as well as overlapping nonempty queries. Do not change source, runner, documentation or these instructions.
