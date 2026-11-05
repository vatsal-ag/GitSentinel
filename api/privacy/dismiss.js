import { privacyState } from './state.js';

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  privacyState.blackout_active = false;
  privacyState.temporarily_dismissed = true;
  privacyState.status = "SNOOZED";

  return res.status(200).json(privacyState);
}
