# Linux container browser check

Checked 2026-09-12 KST after owner authorization to start Colima and download a
browser container image.

- Colima reused its existing VM and started Docker 29.5.2 on Linux arm64.
- Image: `mcr.microsoft.com/playwright:v1.63.0-noble`
- Pulled digest: `sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27`
- Container Node: 24.20.0; bundled Chromium: 153.0.8010.12.

The check used an ephemeral container, disabled its network, mounted this checkout
read-only, and shared IPC as recommended for Chromium stability:

```sh
docker --context colima run --rm --ipc=host --network=none \
  -v "$PWD:/work:ro" -w /work/benchmarks/browser \
  mcr.microsoft.com/playwright:v1.63.0-noble \
  node input-check.mjs /ms-playwright/chromium-1243/chrome-linux-arm64/chrome
```

The command exited 0 with `complete: true` and six observations. Fill and keyboard
inputs, guarded and deliberately broken response ordering, view-disposal mutation,
error/retry recovery, empty-query clearing, and full-document fresh return all
retained their expected rendered outcomes. Submitted browser input remained
trusted and no page errors were observed. The container was removed automatically;
the pulled image and running Colima VM remain on the host.

This resolves the author-side Linux browser-runtime feasibility gap, not the model
screen: those Codex sessions ran macOS Chrome inside workspace-write and both
aborted before page interaction. No model session ran in the container, and no
skill performance result changed. A containerized or otherwise explicitly
permitted model execution path must preserve authentication, sandbox boundaries,
identical baseline/skill inputs, dependency identities and complete resource
accounting before it can replace that blocked evidence.
