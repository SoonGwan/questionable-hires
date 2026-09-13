I’ll use the landlord skill to trace the cookie consumers and scope contracts, then check the decision-changing behavior with local tests and a bounded probe. I’ll preserve existing files and use the specified interpreter without network access.

Domain/path behavior is part of the documented API, and the request, response, and both client implementations use the boundary. Redirects also rebuild cookie headers from the store. I’ll check what a name-only conversion does to those behaviors, alongside the ordinary single-cookie case.

**Keep the `Cookies`/`CookieJar` boundary.** A name-only dictionary cannot preserve supported scope behavior. Its apparent maintenance saving would require rebuilding cookie policy elsewhere or breaking compatibility.

- **Concrete consumers:** [Request construction](project/httpx/_models.py#L403) applies cookie headers; [Response.cookies](project/httpx/_models.py#L835) extracts response cookies. Clients [merge cookie stores](project/httpx/_client.py#L413), persist response cookies in both [sync](project/httpx/_client.py#L1022) and [async](project/httpx/_client.py#L1737) paths, and [rebuild cookies on redirects](project/httpx/_client.py#L475).
- **Supported contracts:** [Documentation](project/docs/quickstart.md#L403) explicitly promises domain/path access. [Scoped lookup](project/httpx/_models.py#L1143) raises `CookieConflict` for ambiguous names; [deletion and clearing](project/httpx/_models.py#L1168) target scopes. [`CookieJar` input and `.jar`](project/docs/api.md#L153) are public API.
- **Maintenance cost:** The roughly 200-line [implementation](project/httpx/_models.py#L1079) maintains mapping conveniences, scope operations, and two compatibility adapters. It delegates extraction and header policy to the standard-library jar. Removing it would move those responsibilities into request/response/client code or require a replacement cookie engine; it removes no third-party dependency.

Runtime verification used the specified interpreter and this checkout, without network:

- **45 tests passed:** complete model-cookie, client-cookie, and redirect test modules, including login/logout cookie expiry.
- A bounded `MockTransport` probe retained four `sid` cookies across two hosts and two paths. Headers selected the correct host/path, included both matching cookies on `/app/page`, excluded `/app` on `/application`, and omitted cookies for an unrelated host. Scoped deletion preserved the other records.
- `dict(cookies)` raised `CookieConflict`. Explicit last-wins flattening lost three records and, when passed through the existing dictionary input API, sent the surviving value to the unrelated host.
- **Single-cookie normal control passed:** dictionary conversion and outgoing headers agreed. A separate secure-cookie control showed conversion discarded the HTTPS restriction.

**Nearest viable alternative:** retain the existing dictionary convenience input, normalized into `Cookies`/`CookieJar` at the boundary. For example, replacing the merge copy with `dict(self.cookies)` already fails on duplicate names; forcing conversion loses scope metadata. Preserving that metadata and its policy recreates the storage responsibility this boundary already centralizes.

The probe demonstrates conversion behavior, not an implemented replacement. Existing files remained unchanged; no dependencies, mutation copies, or diagnostic files were created.
