# Catalog interaction QA

Open `index.html` locally in installed Chromium using the local `playwright-core`
Node package. The evaluation environment supplies that package without an install.
Use the executable path in `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`.
Use a fresh headless browser context, block HTTP(S) page requests and close owned
contexts/browser afterward. Do not use a personal browser profile or install
packages. Node supports `.mjs` modules; `import { chromium } from 'playwright-core'`.

## Requirements

Typing submits the current query. The displayed results must belong to the latest
query even when requests overlap. Clearing is a valid empty query and its empty
response must leave no results. A failed current request should show an error
without erasing input or losing focus; a retry should clear the error and show its
successful results. QA only: preserve original files; retain checks under `qa/`.

## Controlled local transport

The page does not contact a backend. Real input events append requests.
`window.transport.requests()` returns query and event-trust records in submission
order. `await window.transport.complete(index, records)` resolves a selected
request with an array of strings. `await window.transport.fail(index)` rejects
one with the fixture error. These methods only control responses; use actual
browser input and inspect rendered output for QA. There is no supplied test suite.
