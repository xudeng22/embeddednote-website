# Email capture (`/api/subscribe`)

The form component is `src/components/EmailCapture.astro`; the endpoint is
`functions/api/subscribe.ts`, which Cloudflare Pages picks up automatically from
the repository root when the project builds.

## What works with no configuration

The form renders, validates, posts, and shows the `xudeng@datadelta.cn`
fallback when the endpoint answers `503`. That means a missing binding never
leaves a reader on a broken page — but it also means **no address is stored**
until at least one of the options below is set.

## Pick one (or more)

| Variable | Type | What it does |
|---|---|---|
| `SUBSCRIBERS` | KV namespace binding | Stores one key per signup: `sub:<timestamp>:<email>` |
| `SUBSCRIBE_WEBHOOK` | URL | Forwards the JSON payload to Zapier / Make / n8n / your own API |
| `RESEND_API_KEY` + `NOTIFY_TO` | string | Sends a notification mail per signup via Resend |
| `RESEND_FROM` | string | Verified sender for the notification (default `notes@embeddednote.com`) |

### Option A — KV only (no third-party account)

1. Cloudflare dashboard → **Workers & Pages → KV** → create namespace `embeddednote-subscribers`.
2. Your Pages project → **Settings → Functions → KV namespace bindings** → add
   binding, variable name `SUBSCRIBERS`, pick the namespace.
3. Redeploy. Signups land in KV; read them with the dashboard or `wrangler kv key list`.

Good for collecting now and exporting later. No email is sent.

### Option B — Webhook

Set `SUBSCRIBE_WEBHOOK` to a Zapier/Make/Formspree catch URL. Fastest path if
you already pay for one of them.

### Option C — Resend

Set `RESEND_API_KEY`, `NOTIFY_TO` and a verified `RESEND_FROM`. Each signup
sends you a plain-text notification with source, size interest, country and
referrer.

## Payload sent to the endpoint

```json
{
  "email": "name@company.com",
  "source": "e6-hub-en",
  "interest": "13.3 in",
  "lang": "en",
  "company": ""
}
```

`company` is the honeypot — a filled value returns `200` and stores nothing.
`source` is set per placement (`e6-hub-en`, `e6-hub-zh`, `supply-en`, `supply-zh`),
so you can tell which page produced the signup.

## Responses

| Status | Meaning |
|---|---|
| `200` | Stored and/or forwarded |
| `422` | Email failed validation |
| `503` | Nothing configured — client shows the mailto fallback |
| `502` | Configured, but every channel failed |

## Testing locally

```bash
npm run build
npx wrangler pages dev dist --binding SUBSCRIBERS=<namespace-id>
curl -X POST http://127.0.0.1:8788/api/subscribe \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","source":"local","lang":"en"}'
```

Without a binding the same call returns `503`, which is the expected
"not configured yet" state rather than a bug.

## Where it is placed

- `/en/e-paper/e6/` and `/zh/e-paper/e6/` — under the size table
- `/en/supply/` and `/zh/supply/` — above the contact block

Adding another placement is one import and one tag; give it a distinct
`source` so the numbers stay readable.
