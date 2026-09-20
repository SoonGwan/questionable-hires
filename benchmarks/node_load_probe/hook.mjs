// Feasibility probe only. A load record is NOT proof of evaluation or test coverage.
import { registerHooks } from 'node:module';
import { createHash } from 'node:crypto';

const selected = new Set(JSON.parse(process.env.QH_PROBE_MODULE_URLS));
registerHooks({
  load(url, context, nextLoad) {
    const result = nextLoad(url, context);
    if (selected.has(url)) {
      const source = result.source;
      const digest = source == null ? null : createHash('sha256').update(source).digest('hex');
      console.error('QH_LOAD ' + JSON.stringify({ pid: process.pid, url,
        format: result.format, source_sha256: digest }));
    }
    return result;
  },
});
