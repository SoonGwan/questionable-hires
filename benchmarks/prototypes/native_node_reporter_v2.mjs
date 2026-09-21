// Experimental first-look display, not a verdict or a substitute for full TAP.
// Pair with native TAP in the same invocation; caller owns exit/logs/deadline.
const LIMIT = 200;
const WIDTH = 500;

function preview(value) {
  if (value === undefined) return null;
  const text = String(value);
  return text.length <= WIDTH ? text : {prefix: text.slice(0, WIDTH), truncated: true};
}

export default async function* report(source) {
  let summaries = 0, native = null, ordinaryPasses = 0, shown = 0, omitted = 0;
  const events = {};
  const displayedByType = {'test:pass': 0, 'test:fail': 0};
  yield JSON.stringify({view: 'experimental-first-look-v2',
    fields: ['event', 'name', 'file', 'line', 'nesting', 'skip', 'todo', 'message', 'cause'],
    warning: 'Ordinary pass identities omitted. Read same-run full TAP and native exit; this is not verification.'}) + '\n';
  for await (const {type, data} of source) {
    if (type === 'test:summary' && data.file === undefined) {
      summaries++;
      native = {counts: data.counts, success: data.success};
    } else if (type === 'test:pass' || type === 'test:fail') {
      if (type === 'test:pass' && !data.skip && !data.todo) {
        ordinaryPasses++;
        continue;
      }
      // Skip/todo pass events cannot exhaust the separate failure allowance.
      if (displayedByType[type] >= LIMIT) { omitted++; continue; }
      displayedByType[type]++;
      shown++;
      const error = data.details?.error;
      yield JSON.stringify([type, preview(data.name), preview(data.file), data.line ?? null,
        data.nesting ?? null, data.skip ? preview(data.skip) : false,
        data.todo ? preview(data.todo) : false, preview(error?.message),
        preview(error?.cause?.message)]) + '\n';
    } else events[type] = (events[type] || 0) + 1;
  }
  yield JSON.stringify({end: true, summaries, native,
    ordinary_pass_identities_omitted: ordinaryPasses, exceptional_results_shown: shown,
    exceptional_results_omitted: omitted, displayed_by_type: displayedByType, other_events: events,
    warning: 'Missing/duplicate summary or interruption is incomplete. Raw TAP required for identities, diagnostics, stacks and actual/expected.'}) + '\n';
}
