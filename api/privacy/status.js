export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  return res.status(200).json({
    status: "ARMED",
    call_detected: true,
    blackout_active: true,
    active_call_tool: "Apple FaceTime",
    temporarily_dismissed: false,
    native_drm_supported: true,
    cocoa_status: "NSWindowSharingNone (0)"
  });
}

