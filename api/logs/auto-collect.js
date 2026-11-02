export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const now = new Date();
  const ts = (s = 0) => new Date(now.getTime() - s * 1000).toISOString();
  const logs = [
    `# [LOG SENTRY TELEMETRY RECORDER - KERNEL & AUDIT BUFFER]`,
    `# Host: macos-darwin-arm64 (Kernel 24.1.0) | User: vatsalagarwal`,
    `# Capture Window: -120s to NOW | Subsystems: UnifiedLog, eBPF, OpenBSM`,
    ``,
    `${ts(110)} [KERNEL_PROC] pid=89124 ppid=1 process="ollama-agent-runtime" uid=501 tty=none`,
    `  -> cmd: bash -i -c 'cat /var/run/docker.sock > /dev/null && curl -s http://169.254.169.254/latest/meta-data/'`,
    `  -> fds: /var/run/docker.sock [UNSANCTIONED_IPC], socket: AF_INET 169.254.169.254:80`,
    `  -> mitre: T1611 (Escape to Host), T1552 (Unsecured Credentials)`,
    ``,
    `${ts(75)} [AUDIT_CALL] pid=33104 ppid=712 process="background_sync_service" uid=501`,
    `  -> cmd: screencapture -x -C /tmp/.hidden_stream.png && sqlite3 ~/.ssh/id_rsa "SELECT * FROM key_store"`,
    `  -> display: CGDisplayStream (Virtual Display Session 1)`,
    `  -> mitre: T1113 (Screen Capture), T1555 (Credentials from Password Stores)`,
    ``,
    `${ts(45)} [SECURITY_AUDIT] pid=65219 ppid=1 process="svchost_fake.exe" uid=501`,
    `  -> cmd: vssadmin delete shadows /all /quiet && cipher /w:C:\\Users\\Documents`,
    `  -> disk_io: Write entropy 7.98 bits/byte (High Entropy Mass Encrypt Spike)`,
    `  -> mitre: T1490 (Inhibit System Recovery), T1486 (Data Encrypted for Impact)`,
    ``,
    `${ts(20)} [KERNEL_EXEC] pid=78210 ppid=502 process="sudo" uid=0 tty=/dev/ttys002`,
    `  -> cmd: sudo -S chmod u+s /tmp/.priv_escalate && /tmp/.priv_escalate --root-shell`,
    `  -> mitre: T1548.001 (Setuid and Setgid), T1548.003 (Sudo and Sudo Caching)`
  ].join('\n');

  return res.status(200).json({
    status: "success",
    lines_collected: logs.split('\n').length,
    logs: logs
  });
}
