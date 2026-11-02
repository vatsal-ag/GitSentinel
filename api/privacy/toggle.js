export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const tools = ["Apple FaceTime", "Zoom Video Meeting", "Google Meet Session", "Microsoft Teams Meeting", "OBS Studio"];
  const tool = tools[Math.floor(Math.random() * tools.length)];
  return res.status(200).json({
    status: "BLACKOUT_TOGGLED",
    blackout_active: true,
    active_call_tool: tool
  });
}
