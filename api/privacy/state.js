// Shared in-memory state for Vercel Serverless
export const privacyState = {
  status: "ARMED",
  call_detected: false,
  blackout_active: false,
  active_call_tool: null,
  temporarily_dismissed: false,
  native_drm_supported: false
};
