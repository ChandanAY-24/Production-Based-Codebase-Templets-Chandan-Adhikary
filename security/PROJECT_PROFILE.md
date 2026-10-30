# Project Security Profile
Generated: 2026-10-30 by Antigravity Agent
Project: Spec-Driven Development (SDD) & Agentic Coding Framework

## Flags
| Flag | Value | Evidence |
|---|---|---|
| `WEB_FRONTEND` | true | `frontend/index.html`, `frontend/package.json` |
| `BACKEND` | true | `backend/main.py` (Python HTTP server), `src/services.py` |
| `BAAS` | false | No Firebase/Supabase configuration or rules detected |
| `DATABASE` | true | SQLite migrations (`database/migrations/20261030_000000_init_schema.sql`), `connectors/vector-memory/store.py` |
| `HAS_AUTH` | true | `database/migrations/` contains `users` table; `docs/AUTHENTICATION-SECURITY.md` specifies token verification |
| `HAS_ADMIN` | true | `database/migrations/` defines user roles (`architect`, `admin`); `docs/AGENTS.md` and `database/seeds/seed.sql` (`u_admin_01`) |
| `HAS_API` | true | REST routes in `backend/main.py` (`/api/v1/tasks`, `/health`) and contracts in `docs/APIS.md` |
| `GRAPHQL` | false | No GraphQL schemas or resolvers |
| `WEBSOCKETS` | false | No WebSocket or socket.io server |
| `FILE_UPLOAD` | false | No file upload endpoints or multipart handlers |
| `PAYMENTS` | false | `payment/` directory is empty placeholder with `.gitkeep`; no billing SDKs or payment handlers |
| `OUTBOUND_FETCH` | false | No user-controlled outbound HTTP requests |
| `PII` | true | User emails and identifiers in `database/migrations/` and `database/seeds/seed.sql` |
| `SENSITIVE_PII` | false | No government IDs, financial data, health, or biometrics |
| `CHILDREN` | false | Developer toolchain and agent orchestration platform |
| `EU_USERS` | unknown | Developer tooling; jurisdiction not constrained |
| `US_USERS` | unknown | Developer tooling; jurisdiction not constrained |
| `INDIA_USERS` | unknown | Developer tooling; jurisdiction not constrained |
| `ANALYTICS_ADS` | false | No Google Analytics, Meta Pixel, or ad tracking SDKs |
| `EMAIL_SMS` | false | No email or SMS messaging integrations |
| `AI_LLM` | true | `plugins/omniroute-proxy/`, MCP tool servers, agent swarm in `AGENTS.json`, API keys template in `.env.example` |
| `MOBILE_ANDROID` | false | No Android project or Gradle files |
| `MOBILE_IOS` | false | No iOS project or Xcode files |
| `DESKTOP` | false | No desktop wrapper or native binaries |
| `ELECTRON` | false | No Electron dependencies or main processes |
| `GAME` | false | Not a game engine or client |
| `MULTIPLAYER` | false | No multiplayer game netcode |
| `IN_APP_PURCHASE` | false | No mobile or virtual currency store integrations |
| `CONTAINERS` | false | No Dockerfile or Kubernetes manifests present |
| `IAC` | false | No Terraform or CloudFormation manifests |
| `CLOUD` | false | Local standalone Python/Node architecture |
| `CI` | false | No `.github/workflows/` present initially |
| `CMS` | false | No WordPress or CMS engines |
| `PUBLIC_DOMAIN` | false | Local development server target (`localhost:8000`) |

## Stack
- **Languages:** Python 3.14, HTML5/CSS3/JavaScript, Shell (Bash/PowerShell)
- **Frameworks & Runtimes:** Python `http.server`, `unittest`, `pydantic`
- **Package Managers & Lockfiles:** `pip` (`requirements.txt`), `npm` (`package.json`, `frontend/package.json`)
- **Database:** SQLite 3 (`connectors/vector-memory/memory.db`, `database/app.db`)
- **Hosting / Deploy Target:** Standalone daemon / Local Python service
- **Auth Provider:** In-app bearer token / session authentication with cryptographic tokens
- **Payment Provider:** None
- **Third-Party Dependencies:** `pydantic`, `pytest`, `requests`, `python-dotenv`, `flake8`
- **Environments:** `development` (`.env.example`)
- **Test Framework:** Python `unittest` (`python -m unittest discover -s tests -p "test_*.py" -v`) / `pytest`

## Attack surface
### Endpoints
| Method | Path | Auth | Role | Handles PII | Notes |
|---|---|---|---|---|---|
| `GET` | `/health` | None | Public | No | Health check returning `{status: "healthy"}` |
| `GET` | `/api/v1/tasks` | Bearer Token | Any authenticated | No | Lists tasks with `status` filter and `limit` pagination cap |
| `POST` | `/api/v1/tasks` | Bearer Token | Authenticated developer/architect | No | Creates task linked to specification; enforces schema limits |
| `POST` | `/api/v1/verify-patch` | Bearer Token | Authenticated developer/architect | No | Validates patch diff against AST and consensus rules |

### Personal data inventory
| Data | Where stored | Purpose | Shared with | Retention |
|---|---|---|---|---|
| User email | `database/migrations/20261030_000000_init_schema.sql` (`users.email`) | Developer identity & task attribution | None | Retained until user account deletion |
| User ID | `database/migrations/` (`users.id`, `tasks.user_id`) | Foreign key relations and task ownership | None | Cascaded on user deletion |

## Applicable check groups
`SEC`, `AUTH`, `AC`, `INP`, `WEB`, `API`, `SUP`, `INFRA`, `CRYPTO`, `PRIV`, `LOG`, `OPS`, `AI`, `DESIGN`
*(MOB, DESK, GAME are N/A based on project flags)*
