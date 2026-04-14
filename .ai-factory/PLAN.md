# Implementation Plan: Production Readiness Audit and LLM Switching for Telegram Bot

Branch: none
Created: 2026-04-14

## Settings
- Testing: no
- Logging: verbose
- Docs: no

## Commit Plan
- **Commit 1** (after tasks 1-3): `chore: harden bot runtime and provider error handling`
- **Commit 2** (after tasks 4-6): `chore: improve production health checks and deploy workflow`

## Tasks

### Phase 1: Runtime Stability
- [ ] Task 1: Formalize runtime configuration in `bot/config.py` and `bot/main.py` for production-safe operation. Add explicit env-driven settings for `LOG_LEVEL`, provider timeouts, and limited retry counts; validate `LLM_DEFAULT` against supported values; keep startup wiring inside `bot/main.py` per layered architecture.
  Logging requirements: add startup/shutdown logs in `bot/main.py`; log effective non-secret runtime settings at INFO; log invalid config decisions at ERROR; ensure log level is controlled by env and can be reduced without code changes.
  Scope note: treat `yandex` as the default LLM in config and env examples unless the runtime explicitly overrides it.
- [ ] Task 2: Introduce safe provider error classification in `bot/llm_clients/base.py`, `bot/llm_clients/gigachat.py`, `bot/llm_clients/yandex.py`, and update `bot/handlers/main.py` to stop leaking raw upstream errors to Telegram users.
  Logging requirements: log provider name, operation, timeout/network/auth/rate-limit/server error class, and sanitized failure reason; use DEBUG for request lifecycle checkpoints, INFO for major provider calls, and ERROR for failed upstream requests without printing secrets or raw tokens.
- [ ] Task 3: Rework HTTP client lifecycle in `bot/llm_clients/__init__.py`, `bot/llm_clients/gigachat.py`, `bot/llm_clients/yandex.py`, and `bot/main.py` to reuse shared `httpx.AsyncClient` instances and close them gracefully on shutdown.
  Logging requirements: log client initialization and shutdown in `bot/main.py`; log provider client creation/close events at DEBUG; log unexpected lifecycle failures at ERROR.

### Phase 2: Request Safety
- [ ] Task 4: Add bounded resilience in `bot/llm_clients/gigachat.py` and `bot/llm_clients/yandex.py`: minimal retry/backoff only for transient failures (`429`, `5xx`, network timeouts), with conservative limits suitable for a small Telegram bot.
  Logging requirements: log retry attempt number, provider, retry reason, and final outcome; DEBUG for each retry decision, INFO for recovery after retry, ERROR when all retries are exhausted.
- [ ] Task 5: Harden Telegram response flow in `bot/handlers/main.py`: add long-message chunking or safe truncation for Telegram limits, preserve current UX, and keep in-memory state bounded with minimal safeguards rather than introducing persistence.
  Logging requirements: log selected model, user-scoped request handling milestones, and chunking/truncation decisions at DEBUG; log delivery failures at ERROR; avoid logging raw prompt/response bodies unless explicitly sanitized.
- [ ] Task 6: Make LLM switching an explicit supported interaction in `bot/handlers/main.py`, `bot/config.py`, `.env_example`, and user-facing bot text. Reuse the existing `/model` flow, ensure it clearly reports the current model, rejects unavailable providers cleanly, and aligns the default selection with `yandex`.
  Logging requirements: log incoming model-switch requests, chosen provider, fallback decisions, and rejected switches at DEBUG/INFO; log invalid or unavailable provider selections at WARN without exposing secrets.

### Phase 3: Production Checks
- [ ] Task 7: Replace weak import-only health checks with a real self-check path shared by `bot/main.py`, `Dockerfile`, `compose.yml`, `compose.production.yml`, and `deploy/scripts/health-check.sh`. The self-check should validate config and basic application bootstrap without starting polling.
  Logging requirements: log self-check start/result in `bot/main.py`; INFO on successful self-check, ERROR on failed validation with sanitized reason; in shell scripts print only operational status lines, not secrets.
- [ ] Task 8: Strengthen `deploy/scripts/deploy.sh`, `deploy/scripts/update.sh`, and `deploy/scripts/rollback.sh` with minimal production guardrails: check required files, verify env presence, wait for healthy state, and fail clearly when rollout or rollback validation does not pass.
  Logging requirements: print each operational step in scripts, include explicit success/failure checkpoints, and keep output safe for CI logs; no secret values in shell output.

### Phase 4: Final Audit
- [ ] Task 9: Run a final production-readiness pass across `README.md`, `docs/deployment.md`, `docs/configuration.md`, Docker/Compose files, and runtime code to confirm that the bot can be started, checked, and operated with minimal surprises in production.
  Logging requirements: verify that all newly added runtime logs go to stdout/stderr, respect `LOG_LEVEL`, and do not expose secrets; document any residual risks directly in the final review notes rather than adding broad new features.
