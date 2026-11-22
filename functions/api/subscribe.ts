/**
 * POST /api/subscribe — Cloudflare Pages Function.
 *
 * Storage and delivery are deliberately pluggable, because the right provider
 * depends on what the account already has. Configure any combination:
 *
 *   SUBSCRIBERS        KV namespace binding  — append {email, source, ts, ...}
 *   SUBSCRIBE_WEBHOOK  URL                   — forward the JSON payload
 *   RESEND_API_KEY     string                — send a notification mail
 *   NOTIFY_TO          address               — recipient for the notification
 *   RESEND_FROM        address               — verified sender, e.g. xudeng@datadelta.cn
 *
 * With none of them set the endpoint answers 503 and the client shows the
 * mailto fallback, so the page never looks broken.
 */

interface Env {
  SUBSCRIBERS?: any;
  SUBSCRIBE_WEBHOOK?: string;
  RESEND_API_KEY?: string;
  NOTIFY_TO?: string;
  RESEND_FROM?: string;
}

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

function thanksPage(lang: string): Response {
  const zh = lang === 'zh';
  const html = `<!doctype html><html lang="${zh ? 'zh-CN' : 'en'}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>${zh ? '已订阅' : 'Subscribed'}</title>
<style>body{font:16px/1.7 system-ui,sans-serif;max-width:34rem;margin:18vh auto;padding:0 1.5rem;color:#17211e}
a{color:#b94530}</style></head><body>
<h1>${zh ? '已收到' : 'Got it'}</h1>
<p>${zh ? '规格书会发到你的邮箱。' : 'The spec sheets are on their way to your inbox.'}</p>
<p><a href="/${lang}/e-paper/e6/">${zh ? '返回' : 'Back to'} ${zh ? 'E6 尺寸页' : 'the E6 sizes'}</a></p>
</body></html>`;
  return new Response(html, { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}

export const onRequestPost = async (context: { request: Request; env: Env }): Promise<Response> => {
  const { request, env } = context;
  const contentType = request.headers.get('content-type') ?? '';
  const wantsJson = contentType.includes('application/json');

  let payload: Record<string, unknown> = {};
  try {
    if (wantsJson) {
      payload = (await request.json()) as Record<string, unknown>;
    } else {
      const form = await request.formData();
      payload = Object.fromEntries(form.entries());
    }
  } catch {
    return json({ ok: false, message: 'Could not read the submission.' }, 400);
  }

  const email = String(payload.email ?? '').trim().toLowerCase();
  const source = String(payload.source ?? 'unknown').slice(0, 80);
  const interest = String(payload.interest ?? '').slice(0, 80);
  const lang = String(payload.lang ?? 'en');
  const honeypot = String(payload.company ?? '').trim();

  // Bots fill the hidden field; answer 200 so they do not retry.
  if (honeypot) return json({ ok: true, ignored: true });

  if (!EMAIL.test(email) || email.length > 254) {
    return json({ ok: false, message: 'That email address does not look right.' }, 422);
  }

  const record = {
    email,
    source,
    interest,
    lang,
    ts: new Date().toISOString(),
    country: request.headers.get('cf-ipcountry') ?? '',
    referer: request.headers.get('referer') ?? ''
  };

  const configured = Boolean(env.SUBSCRIBERS || env.SUBSCRIBE_WEBHOOK || env.RESEND_API_KEY);
  if (!configured) {
    return json(
      {
        ok: false,
        configured: false,
        message: 'No subscriber store is configured yet.'
      },
      503
    );
  }

  const results: Record<string, string> = {};

  if (env.SUBSCRIBERS) {
    try {
      await env.SUBSCRIBERS.put(`sub:${record.ts}:${email}`, JSON.stringify(record));
      results.store = 'ok';
    } catch (error) {
      results.store = `failed: ${String(error)}`;
    }
  }

  if (env.SUBSCRIBE_WEBHOOK) {
    try {
      const response = await fetch(env.SUBSCRIBE_WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(record)
      });
      results.webhook = response.ok ? 'ok' : `http ${response.status}`;
    } catch (error) {
      results.webhook = `failed: ${String(error)}`;
    }
  }

  if (env.RESEND_API_KEY && env.NOTIFY_TO) {
    try {
      const response = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: env.RESEND_FROM ?? 'EmbeddedNote <xudeng@datadelta.cn>',
          to: [env.NOTIFY_TO],
          subject: `Spec-sheet request: ${email}`,
          text: [
            `Email:    ${record.email}`,
            `Source:   ${record.source}`,
            `Interest: ${record.interest || '(not given)'}`,
            `Language: ${record.lang}`,
            `Country:  ${record.country}`,
            `Time:     ${record.ts}`,
            `Referer:  ${record.referer}`
          ].join('\n')
        })
      });
      results.mail = response.ok ? 'ok' : `http ${response.status}`;
    } catch (error) {
      results.mail = `failed: ${String(error)}`;
    }
  }

  // Auto-reply with the four frame briefs, in the language the form was in.
  if (env.RESEND_API_KEY && env.NOTIFY_TO) {
    const zh = record.lang === 'zh';
    const REPLY_BRIEFS = [
      { label: '7.09 in', file: zh ? 'e6-frame-7.09in.pdf' : 'e6-frame-7.09in-en.pdf' },
      { label: '10 in', file: zh ? 'e6-frame-10in.pdf' : 'e6-frame-10in-en.pdf' },
      { label: '13.3 in', file: zh ? 'e6-frame-13.3in.pdf' : 'e6-frame-13.3in-en.pdf' },
      { label: '31.5 in', file: zh ? 'e6-frame-31.5in.pdf' : 'e6-frame-31.5in-en.pdf' }
    ];
    const links = REPLY_BRIEFS.map(
      (item) => `· ${item.label} — https://embeddednote.com/downloads/e6-frame/${item.file}`
    ).join('\n');
    const text = zh
      ? `谢谢索取。四份 E6 相框方案书在这里:\n\n${links}\n\n每一份写的是我们实际在做的 TCON、供电和结构,不是数据手册的复述。\n\n电子纸工程笔记每两周一封。要样品或报价,直接回这封信,写清尺寸和数量即可。\n\n— Deng Xu, EmbeddedNote`
      : `Thanks for asking. The four E6 frame briefs are here:\n\n${links}\n\nEach one covers the TCON, the power rail and the enclosure we actually build, rather than a datasheet reprint.\n\nThe engineering notes follow every two weeks. For samples or a quote, reply to this address with the panel size and the quantity.\n\n— Deng Xu, EmbeddedNote`;
    try {
      const response = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: env.RESEND_FROM ?? 'EmbeddedNote <xudeng@embeddednote.com>',
          to: [record.email],
          subject: zh ? 'E6 相框方案书' : 'Your E6 frame briefs',
          text
        })
      });
      results.reply = response.ok ? 'ok' : `http ${response.status}`;
    } catch (error) {
      results.reply = `failed: ${String(error)}`;
    }
  }

  const anySuccess = Object.values(results).some((value) => value === 'ok');

  if (!wantsJson) {
    return anySuccess ? thanksPage(lang) : json({ ok: false, results }, 502);
  }
  return anySuccess
    ? json({ ok: true, results })
    : json({ ok: false, message: 'The subscriber store rejected the request.', results }, 502);
};

export const onRequestGet = async (): Promise<Response> =>
  json({ ok: false, message: 'POST an email to this endpoint.' }, 405);
