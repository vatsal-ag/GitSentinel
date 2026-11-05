import { privacyState } from './state.js';

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  privacyState.blackout_active = !privacyState.blackout_active;
  privacyState.call_detected = privacyState.blackout_active;
  privacyState.temporarily_dismissed = false;
  privacyState.active_call_tool = privacyState.blackout_active ? "Apple FaceTime" : null;
  privacyState.status = privacyState.blackout_active ? "CALL_DETECTED" : "ARMED";

  return res.status(200).json(privacyState);
}
