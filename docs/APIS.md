# APIS: OpenAPI Contracts, Endpoints & Serializers
> Standard: OpenAPI 3.1.0 Contract
> Base URL: `http://localhost:8000/api/v1`

---

## 1. Global Response Envelope
All API endpoints return JSON conforming to the standard envelope:
```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "timestamp": "2026-10-30T00:00:00Z",
    "requestId": "req_uuid_v4"
  }
}
```

---

## 2. Core Endpoints

### 2.1 Tasks API
- **`GET /api/v1/tasks`**
  - **Description:** Retrieve list of active agent tasks.
  - **Query Params:** `status` (optional: PENDING, IN_PROGRESS, VERIFIED), `limit` (default: 20).
  - **Response:** Array of `AgentTask` objects.

- **`POST /api/v1/tasks`**
  - **Description:** Create a new task linked to a spec requirement.
  - **Payload:**
    ```json
    {
      "title": "Implement authentication token refresher",
      "specReference": "docs/SPEC.md#L45",
      "invariants": ["Tokens must rotate on refresh", "Old tokens must be invalidated"]
    }
    ```
  - **Response Status:** `201 Created`

### 2.2 Verification API
- **`POST /api/v1/verify-patch`**
  - **Description:** Submits a diff patch to AST and consensus review gates.
  - **Payload:**
    ```json
    {
      "patch": "diff --git a/... b/...",
      "targetFile": "src/auth.py",
      "runTests": true
    }
    ```
  - **Response Status:** `200 OK`
