# OpenClaw Daemon Connector
> Reference: [20. openclaw]
> Purpose: Sandboxed background task runner and worker daemon

---

## Capabilities
- Executes long-running background tasks (e.g. headless Playwright runs, AST scans, batch data migrations) without blocking interactive agent conversational threads.
- Isolates subprocess execution and captures structured execution logs.
- Can be started with `python connectors/openclaw-daemon/daemon.py` or inspected with `--once`.
