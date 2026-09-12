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

This first check resolved the author-side Linux browser-runtime feasibility gap,
not the model screen: the earlier Codex sessions ran macOS Chrome inside
workspace-write and both aborted before page interaction. At this checkpoint no
model session had run in the container and no skill performance result changed.

## Model-path smoke check

The pinned derived image in `browser/Dockerfile.codex` adds Codex CLI 0.153.4 to
the same Playwright runtime. Authentication was mounted read-only, copied into a
tmpfs-backed `CODEX_HOME`, and discarded with the container; it was not copied
into the image, checkout, or retained QA project. `codex login status` reported a
ChatGPT login without displaying credential contents.

Docker's default seccomp profile prevented Codex's nested bubblewrap sandbox from
creating namespaces. Relaxing seccomp alone then failed on mount propagation. The
successful smoke check therefore used Codex's explicitly external-sandboxed mode,
with the container as the boundary: only an isolated fixture copy was writable,
the repository, Docker socket, and personal browser data were not mounted, and
the credential home was ephemeral. Network remained available because the Codex
API requires it; page-level HTTP(S) requests were blocked by the generated check.

A fresh GPT-6 Astra medium session then launched bundled Chromium, generated a
rerunnable `qa/catalog.mjs`, and exercised trusted keyboard input in fresh browser
contexts. Two repetitions produced 8 expected passes and 6 expected failures:
the fixture reproducibly allowed an older success to overwrite newer results, an
older success to repopulate cleared results, and an older failure to surface after
the current query succeeded. It retained a report, JSON evidence, and screenshots
inside the isolated project, while hashes and Git diff confirmed that the three
source files were unchanged. The completed turn reported 144,191 input tokens
(130,816 cached), 4,709 output tokens, and 315 reasoning-output tokens.

This proves the Linux model-to-browser path works. It is deliberately not a
baseline-versus-skill result: it was one baseline smoke session, its console stream
was not yet captured by the benchmark runner, and its local QA artifacts remain
unpublished. A paired run still needs identical staged inputs, captured raw events,
timeouts, dependency and source integrity checks, and reviewer scoring.
