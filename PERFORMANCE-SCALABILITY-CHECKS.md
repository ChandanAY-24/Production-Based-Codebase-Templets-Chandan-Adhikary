# PERFORMANCE & SCALABILITY MAINTENANCE CHECKS
> **Primary Specification:** [docs/PERFORMANCE-SCALABILITY-CHECKS.md](docs/PERFORMANCE-SCALABILITY-CHECKS.md)  
> **Status:** ACTIVE & MANDATORY FOR ALL AGENT DEPLOYMENTS

Please refer to the full enterprise specification in:
👉 **[docs/PERFORMANCE-SCALABILITY-CHECKS.md](docs/PERFORMANCE-SCALABILITY-CHECKS.md)**

---

## The 15 Core Distributed Systems Pillars
1. **Scalability:** Stateless compute, connection pool bounds, database sharding.
2. **Availability:** Multi-AZ redundancy, 99.99% SLA, liveness & readiness health probes.
3. **Reliability:** Idempotency keys (`Idempotency-Key`), atomic rollbacks, strict schema validation.
4. **Fault Tolerance:** Graceful degradation, N+1 redundancy, circuit breaker protection.
5. **Resilience:** Jittered exponential backoff, bulkheads, sliding-window rate limiting.
6. **Latency:** API p95 $\le 500\text{ ms}$, p99 $\le 1000\text{ ms}$, L1/L2/L3 multi-tier caching.
7. **Throughput:** Async non-blocking I/O, database batching, backpressure management.
8. **Consistency:** Strong vs Eventual consistency matrix, quorum consensus ($R + W > N$).
9. **Durability:** Write-Ahead Logging (WAL), multi-region replication, verified snapshot restores.
10. **Partition Tolerance:** Raft/Paxos consensus ($\ge 3$ nodes), fencing tokens on distributed locks.
11. **CAP Theorem:** Documented CP vs AP trade-offs and PACELC latency considerations.
12. **Load Balancing:** Layer 4/7 balancing (Least Connections / Round-Robin), TLS offloading, no sticky sessions.
13. **Horizontal Scaling:** Shared-nothing architecture, object storage for assets, dynamic discovery.
14. **Vertical Scaling:** Headroom monitoring, file descriptor limits ($\ge 65536$), OOM prevention.
15. **Auto Scaling:** Multi-metric triggers (CPU, RAM, queues), stabilization cooldowns, warm pools.

---

## Deployment Archetypes
Agents must identify and adhere to the target deployment archetype before code generation:
- **Tier A:** Serverless & Edge (Cloud Run, Lambda, Workers)
- **Tier B:** Containerized Microservices & Kubernetes (EKS, GKE, ECS)
- **Tier C:** Monolithic VM / High Compute (FastAPI, Django, Express on EC2/GCE)
- **Tier D:** Real-Time Event-Driven & Streaming (Kafka, WebSockets, RabbitMQ)
- **Tier E:** Distributed Data & AI Inference (Vector DBs, PyTorch/vLLM)

