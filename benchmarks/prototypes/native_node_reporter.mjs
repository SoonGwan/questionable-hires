// Experimental display only. Pair with the native TAP reporter in the SAME run.
// Does not execute tests, change exit status, retain logs, or establish assertions.
const MAX_RESULTS = 200;
const MAX_TEXT = 500;

function preview(value) {
  if (value === undefined) return undefined;
  const text = String(value);
  return {text: text.slice(0, MAX_TEXT), truncated: text.length > MAX_TEXT};
}

export default async function* report(source) {
  let summaries = 0, finalSummary, resultCount = 0, omittedResults = 0;
  const otherEvents = {};
  yield JSON.stringify({type: 'notice', experimental: true,
    limitation: 'Display excerpt only. Inspect native exit and same-run full TAP. Skips, file-level success and zero assertions do not prove behavior.'}) + '\n';
  for await (const {type, data} of source) {
    if (type === 'test:summary' && data.file === undefined) {
      summaries++;
      finalSummary = {counts: data.counts, native_success: data.success};
    } else if (type === 'test:pass' || type === 'test:fail') {
      resultCount++;
      if (resultCount > MAX_RESULTS) {
        omittedResults++;
        continue;
      }
      const error = data.details?.error;
      yield JSON.stringify({type, name: preview(data.name), file: preview(data.file),
        line: data.line, column: data.column, nesting: data.nesting,
        test_number: data.testNumber, skip: data.skip || false, todo: data.todo || false,
        kind: data.details?.type,
        error: error ? {message: preview(error.message), code: preview(error.code),
          failure_type: preview(error.failureType), cause: preview(error.cause?.message)} : undefined}) + '\n';
    } else {
      otherEvents[type] = (otherEvents[type] || 0) + 1;
    }
  }
  yield JSON.stringify({type: 'end', stream_ended: true,
    global_summary_count: summaries, single_global_summary_seen: summaries === 1,
    observed_result_events: resultCount, omitted_result_events: omittedResults,
    other_event_counts: otherEvents, native: finalSummary,
    limitation: 'Not a pass verdict. Raw TAP includes omitted stacks, actual/expected values, output and diagnostics. Missing summary or interrupted output is incomplete.'}) + '\n';
}
