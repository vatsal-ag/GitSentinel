export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const text = (req.body && req.body.raw_logs) || '';
  let count = 0;
  const sanitized = text
    .replace(/ghp_[A-Za-z0-9]{30,}/g, () => { count++; return '[REDACTED_GITHUB_TOKEN]'; })
    .replace(/github_pat_[A-Za-z0-9_]{30,}/g, () => { count++; return '[REDACTED_GITHUB_PAT]'; })
    .replace(/AKIA[0-9A-Z]{16}/g, () => { count++; return '[REDACTED_AWS_ACCESS_KEY]'; })
    .replace(/-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+PRIVATE KEY-----/g, () => { count++; return '[REDACTED_PRIVATE_KEY]'; })
    .replace(/eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+/g, () => { count++; return '[REDACTED_JWT_TOKEN]'; })
    .replace(/(password|secret|bearer|token)\s*[:=]\s*['"]?[^\s'";]+['"]?/gi, (m) => { count++; return m.split(/[:=]/)[0] + ': [REDACTED_SECRET]'; });

  return res.status(200).json({
    status: "success",
    redactions_made: count,
    sanitized_text: sanitized
  });
}
