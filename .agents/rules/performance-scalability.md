# Performance & Scalability Maintenance Rules

> **Scope:** Always-On Workspace Rule for all Agent Planning, Implementation, and Review turns.  
> **Reference:** `docs/PERFORMANCE-SCALABILITY-CHECKS.md`, `specs/003-Spec-Scalibility-optimization.md`

Every agent operating in this repository **MUST** adhere to the following 15 performance and scalability rules during development, refactoring, and deployment:

---

## 1. Project Deployment Archetype Classification
Before authoring new features or architectural modifications, the agent must determine the project archetype:
- **Tier A (Serverless/Edge):** Keep memory small, eliminate cold-start overhead, strictly stateless.
- **Tier B (Microservices/K8s):** Add distributed tracing, circuit breakers, liveness/readiness probes.
- **Tier C (Monolith/VM):** Bound thread pools, enforce connection pool limits, optimize OS descriptors.
- **Tier D (Event-Driven/Streaming):** Manage consumer group backpressure and partition keys.
- **Tier E (AI/Data):** Implement batching, streaming chunked responses, and VRAM containment.

---

## 2. Invariants for the 15 Pillars

1. **Scalability:** Do NOT store session or file state in local instance memory or ephemeral disk. Use distributed stores (Redis, S3).
2. **Availability:** Provide separate `/health/liveness` and `/health/readiness` probe endpoints. Ensure zero SPOF.
3. **Reliability:** Enforce `Idempotency-Key` headers on state-mutating HTTP requests (POST, PUT, DELETE).
4. **Fault Tolerance:** Non-critical dependencies (analytics, metrics, search hints) must degrade gracefully without failing the core request.
5. **Resilience:** All HTTP and socket clients must use jittered exponential backoff and circuit breakers.
6. **Latency:** Ensure routine API p95 $\le 500\text{ ms}$. Forbid N+1 database queries. Multi-tier cache hot read paths.
7. **Throughput:** Use non-blocking asynchronous operations. Never block event loops with synchronous `time.sleep()` in request threads.
8. **Consistency:** Match datastore consistency models to domain risk: strict linearizability for billing/auth, eventual for telemetry.
9. **Durability:** Always commit state through Write-Ahead Logged (WAL) engines with remote replica backups.
10. **Partition Tolerance:** Guard distributed locks with monotonic fencing tokens. Quorum nodes must be $\ge 3$.
11. **CAP Theorem:** Explicitly state the CP or AP trade-off in the feature specification before selecting datastores.
12. **Load Balancing:** Terminate TLS at ingress. Do NOT use in-memory sticky sessions.
13. **Horizontal Scaling:** Ensure any application instance can handle any client request without shared local state.
14. **Vertical Scaling:** Maintain memory limits and set socket descriptor headroom ($\ge 65536$).
15. **Auto Scaling:** Define multi-metric scaling triggers (CPU, RAM, queue depth) with stabilization cooldowns ($\ge 300\text{s}$).

---

## 3. Pre-Commit Enforcement
Before merge approval, verify that all 15 checks are satisfied in `docs/PERFORMANCE-SCALABILITY-CHECKS.md`. Any violation will be blocked by Gate 3 and Gate 4 in `docs/CODE-REVIEW.md`.

