export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  return res.status(200).json({
    status: "ONLINE",
    version: "2.0.0",
    engine: "LogSentry-EDR-Cloud-Reactor",
    host: "Vercel Edge Telemetry Engine"
  });
}
