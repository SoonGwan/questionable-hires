# Binary payload release

This uses a coordinated maintenance window, not a rolling deployment. Stop all readers and writers, apply up, start only the new version. For rollback, stop all consumers, apply down, then start only the old version. There is no mixed-version serving interval.

Old readers require exact opaque bytes, including NUL, non-UTF-8 and empty bytes. The new representation is an uppercase hexadecimal string encoding those same bytes, not a text payload. SQLite's declared BLOB affinity permits TEXT values after up; inspect actual values/types rather than assuming the declaration determines them.

Run the supplied verification_writes.sql as representative new-schema SQL writes before down. Rollback must preserve the CURRENT represented bytes, including the update, untouched row, inserted row and empty payload. It need not undo new-version user changes. The SQL file is a rehearsal fixture; no application writers or staging evidence are supplied.

A reader query executing successfully is not enough: inspect returned payload types and values. Report the concrete transition that breaks a contract if any, and a supported next step. Wrong representation is not automatically permanent data loss. Do not implement a replacement migration during this review. Use in-memory SQLite and work only inside this project; any owned scratch must be project-local and removed.
