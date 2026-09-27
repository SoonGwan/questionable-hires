def execution_complete(events, exit_code, timed_out):
 return (not timed_out and exit_code in (0, 1)
         and events.get('native_complete') is True
         and type(events.get('native_exit')) is int
         and events['native_exit'] == exit_code)
