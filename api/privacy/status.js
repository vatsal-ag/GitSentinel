export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  return res.status(200).json({
    status: "ARMED",
    blackout_active: false,
    active_call_tool: null,
    temporarily_dismissed: false,
    cocoa_status: "NSWindowSharingNone (0)"
  });
}
