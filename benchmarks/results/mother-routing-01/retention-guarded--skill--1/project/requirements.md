Suggestions is a local async component, not a rendered browser UI.
search(term, request) fetches and stores the returned payload directly. A previously
displayed result must remain visible while the latest request is pending, including
when an older pending request completes. Once the latest request succeeds its
payload must remain visible even if an older response arrives later. Starting a
request must not erase the existing display. Distinct overlapping query strings
are sufficient here. Failure handling, caching, cancellation policy and browser
rendering are outside this task; clean up your own controlled test operations.
