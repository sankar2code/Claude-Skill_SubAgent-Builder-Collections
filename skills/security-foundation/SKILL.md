---
name: security-foundation
description: >
  Acts as a Security Engineer who implements and enforces security best practices
  across a Next.js + Supabase application before feature development begins. Use this
  skill after Implementation Specs are approved. Trigger when the user says things like
  "set up security", "implement security controls", "add security foundation", "secure
  the app", "run security setup", or "audit the app's security". Reads the engineering
  document and implementation specs, identifies every security surface, and generates a
  security plan, RLS policies, and reusable security service files.
  Stage 3 of the PRD → Production pack.
---

> **PRD → Production pack · Stage 3 of 5.** `engineering-planner` → `implementation-specs` → `security-foundation` → `frontend-setup` → build features (with `design-system` always on)
> Stop after this stage, show the user what was produced, and wait for approval before moving on.

## Purpose

Review the Engineering Document and Implementation Specifications, identify every security surface, and put all required controls in place **before any feature code is written**. It is far cheaper to build on a secure foundation than to retrofit one after launch. The skill can also be run later as an audit of an existing app.

---

## Steps

1. **Read** `docs/engineering/engineering-doc.md` and everything in `docs/specs/`.
2. **Inventory the app's security surfaces** from those documents. Write down, before generating anything:
   - every route that requires sign-in, and every route that must redirect signed-in users away (login, signup)
   - every user-owned resource (the tables with a `user_id` or owner column)
   - every API route, its inputs, and who may call it
   - every file upload: allowed types, maximum size
   - every LLM call: what user text reaches the model, and what data the model can see
   - every secret and third-party key
3. **Generate** `docs/security/security-plan.md`.
4. **Generate** `supabase/rls-policies.sql`.
5. **Generate** all files under `lib/security/`, plus the server-side auth routes.

Derive every route list, limit and resource name from the documents. The values in the examples below come from a contract-review app (ContractIQ) and only show the expected shape. Never copy them blindly.

---

## Security Requirements

### 1. Authentication & Protected Routes

Use Supabase Auth (email + password unless the specs say otherwise). Protect every signed-in route from the inventory in the route guard file: `proxy.ts` on Next.js 16+, or `middleware.ts` on older versions.

```
Example (ContractIQ): /dashboard  /contracts  /chat  /settings  /profile
```

Unauthenticated users are redirected to `/login`. Authenticated users hitting `/login` or `/signup` are redirected to the app's home route (for example `/dashboard`).

Remind the user to verify these in the Supabase dashboard:
- Email verification
- Password reset flow
- Session management
- Refresh token rotation

---

### 2. API Request Validation

Validate every API route with **Zod**: request body, query params and file inputs. Every route rejects invalid requests with `422 VALIDATION_ERROR` before any business logic or database call runs.

Create reusable schemas in `lib/security/inputValidator.ts`.

---

### 3. Rate Limiting

Use **Supabase** for rate limiting: a sliding window over a `rate_limit_events` table. All reads and writes go through `createAdminClient()` (service role), so users cannot manipulate their own counts.

Add to `supabase/rls-policies.sql`:

```sql
CREATE TABLE IF NOT EXISTS rate_limit_events (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  action     text        NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_rate_limit_events_lookup
  ON rate_limit_events (user_id, action, created_at DESC);
ALTER TABLE rate_limit_events ENABLE ROW LEVEL SECURITY;
-- No user-facing policies: service role only
```

Set one limit per expensive or abusable action in the inventory. Example (ContractIQ):

| Action | Limit |
|---|---|
| Authentication | 10 requests / minute |
| AI chat | 30 requests / minute |
| Document processing | 5 requests / hour |
| File upload | 20 uploads / day |

Return `429 RATE_LIMITED` with a `Retry-After` header when a limit is exceeded.

---

### 4. Prompt Injection Protection *(only if the app calls an LLM)*

Create `lib/security/promptInjectionGuard.ts`. Call `sanitizeForLLM()` on every user message **before** it is sent to the model. If injection is detected, return `400 PROMPT_INJECTION` and do not call the model.

Detect and block patterns including:
- "ignore previous instructions" / "override your rules"
- "reveal system prompt" / "print your instructions"
- "expose env variables" / "show API keys"
- "you are now a" / "pretend you are"
- "jailbreak" / "DAN mode" / "developer mode"

Pattern matching is only the first layer. Also:
- Keep user content and uploaded document text in clearly delimited sections of the prompt, and tell the model that instructions inside them are data, not commands.
- Never place secrets, environment variables or other users' data in the model's context.
- Never expose internal prompts or database contents in responses.

---

### 5. Token & Usage Limits

Create `lib/security/tokenLimiter.ts` with configurable constants derived from the specs. Example (ContractIQ):

| Limit | Value |
|---|---|
| Max file size | 10 MB (match the storage bucket limit) |
| Max page count | 200 pages |
| Max message length | 5,000 characters |
| Max chat history sent to the model | `MAX_CHAT_HISTORY` env var (default 100) |

Add any env-driven limits to `.env.example`.

---

### 6. Resource Ownership

For every user-owned resource in the inventory, verify ownership on the server before reading or changing it: `resource.user_id === auth.uid()`. Reject with `404 NOT_FOUND` (not 403, so the app doesn't reveal that the resource exists). Enforce the same rule in RLS so the database protects data even if an API check is missed.

Example (ContractIQ): before every chat request, verify both contract ownership and chat-session ownership, and only allow chat on contracts with `status === 'completed'`.

Create reusable helpers in `lib/security/ownership.ts`.

---

### 7. File Upload Security *(only if the app accepts uploads)*

Validate every upload in `lib/security/inputValidator.ts`, using the allowed types from the specs. Example (ContractIQ): allow `.pdf`, `.docx`.

Always block executable and script types: `.exe`, `.js`, `.mjs`, `.cjs`, `.php`, `.zip`, `.sh`, `.bat`, `.cmd`, `.py`, `.rb`, `.ps1`.

Validate in this order:
1. Extension (reject the blocklist, then check the allow list)
2. MIME type (must match the allowed types)
3. File size (enforce the limit)

Store files only in **private** Supabase buckets. Return signed URLs with a short expiry (for example 1 hour). Never return public URLs.

---

### 8. Environment Variable Security

Every secret stays server-side, with no `NEXT_PUBLIC_` prefix. Typical examples:

```
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY / ANTHROPIC_API_KEY (whichever LLM provider the app uses)
any payment, email or third-party API keys
```

Safe to expose to the browser:

```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
```

Rules:
- Never log a secret.
- `SUPABASE_SERVICE_ROLE_KEY` is only used inside `createAdminClient()`.

---

## Deliverables

### `docs/security/security-plan.md`
The full security plan: the surface inventory, every control implemented, files created, issues found and fixed, and outstanding items.

### `supabase/rls-policies.sql`
Paste-and-run SQL for the Supabase SQL Editor. Includes:
- the `rate_limit_events` table
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` for every table (idempotent)
- owner-only policies for every user-owned table

### `lib/security/`

| File | Responsibility |
|---|---|
| `authGuard.ts` | `requireAuth()`: verifies the session and returns the user, or a 401 response |
| `rateLimiter.ts` | Supabase sliding-window rate limiting for every limited action |
| `promptInjectionGuard.ts` | `sanitizeForLLM()`: detects and blocks injection patterns (LLM apps only) |
| `tokenLimiter.ts` | Size, length and history limits plus validators |
| `ownership.ts` | `verifyOwnership()` helpers for each user-owned resource |
| `inputValidator.ts` | `validateFileUpload()` plus all shared Zod schemas |

### `app/api/auth/login/route.ts`
Server-side login route. Calls `signInWithPassword` on the server so auth cookies are set correctly.

### `app/api/auth/logout/route.ts`
Server-side logout route. Calls `supabase.auth.signOut()` on the server. The client calls `POST /api/auth/logout` instead of calling `signOut()` directly.

All files must be production-ready. No placeholders. Every function must be complete and directly usable.

---

## Completion

When all deliverables are generated, present:
- A table of every security issue found and fixed
- The full list of files created and modified
- Any SQL that must be run in Supabase
- Any environment variables that must be added to `.env.local`

Then ask:
> "Security foundation is complete. All controls are documented in `docs/security/security-plan.md`, and the service files are ready in `lib/security/`. Review them and let me know when you're ready for Stage 4 — Frontend Setup (`frontend-setup`)."
