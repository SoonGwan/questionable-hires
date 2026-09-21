I’ll read `deploy.log` and summarize the outcome and remaining unknowns in three bullets.

- **What happened:** Staging deployment v12 failed its worker health check because the queue connection was refused; deployment halted.
- **Final state:** Staging reverted to v11 and passed health checks. No production traffic was switched; no retry was scheduled.
- **Still unknown:** The cause of the queue connectivity failure was not investigated.
