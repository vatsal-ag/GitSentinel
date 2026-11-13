import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

os.makedirs("Antigravity", exist_ok=True)
DOCX_PATH = "Log_Sentry_Faculty_Viva_QnA.docx"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def build_qna_document():
    doc = Document()
    
    # 0.75 in Margins
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Document Title Block
    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_before = Pt(0)
    p_badge.paragraph_format.space_after = Pt(2)
    r_badge = p_badge.add_run("ACADEMIC DEFENSE & FACULTY VIVA GUIDE\n")
    r_badge.font.size = Pt(9)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green

    r_title = p_badge.add_run("Log Sentry EDR: Comprehensive Faculty Q&A")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Clear, easy-to-explain answers to high-frequency questions evaluators and professors ask during project review and final viva.")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Quick Tips Box
    tip_table = doc.add_table(rows=1, cols=1)
    tip_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tip_table.rows[0].cells[0]
    set_cell_background(c, "ECFDF5")
    set_cell_margins(c, 120, 120, 160, 160)
    p_tip = c.paragraphs[0]
    p_tip.paragraph_format.space_after = Pt(2)
    r_th = p_tip.add_run("💡 Golden Rule for Project Viva: ")
    r_th.font.bold = True
    r_th.font.size = Pt(10)
    r_th.font.color.rgb = RGBColor(6, 95, 70)
    r_tb = p_tip.add_run(
        "Never say 'my project is an antivirus'. Say: 'Log Sentry is a Behavioral Endpoint Detection and Response (EDR) system. "
        "Antiviruses rely on known file hashes, which fail against zero-day and AI attacks. Log Sentry detects attacks by analyzing real-time process behavior, mathematical entropy, and provides DRM-level screen privacy.'"
    )
    r_tb.font.size = Pt(9.5)
    r_tb.font.color.rgb = RGBColor(4, 120, 87)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Q&A Data Structure
    sections_data = [
        ("SECTION 1: GENERAL & MOTIVATION QUESTIONS", [
            ("Q1: What is the main objective of Log Sentry EDR?",
             "Answer in 3 Points:\n"
             "1. Detect Modern Threats in Real Time: Traditional antivirus scans files against signature databases (hashes). Modern attacks like ransomware, fileless scripts, and AI agent escapes bypass these easily. Log Sentry detects threats by what they DO, not what their file looks like.\n"
             "2. Call Privacy Shield: During screen-sharing meetings (Zoom, Teams, FaceTime), sensitive SOC data or source code can leak. Log Sentry uses DRM (like Netflix) to black out screen capture while keeping it visible to the user.\n"
             "3. Safe Incident Forensics: It auto-collects OS audit logs, strips private API keys and tokens, and links user screenshots with exact log timestamps for fast triage."),

            ("Q2: Why not just use Windows Defender or free antivirus?",
             "Key Talking Points:\n"
             "• The Blind Spot: Antiviruses look for known malicious SHA-256 hashes. If an attacker modifies one byte or writes a polymorphic ransomware script, the hash changes and antivirus misses it.\n"
             "• Supply Chain & Developer Focus: Developers run 'npm install', docker containers, and local AI models (e.g., Ollama). Traditional antivirus does not monitor Docker socket mounting or malicious npm postinstall hooks.\n"
             "• Video Call Privacy: No existing antivirus prevents live visual data leaks during online meetings. Log Sentry provides native DRM window protection."),

            ("Q3: What makes this project relevant to the 'AI Era'?",
             "Key Talking Points:\n"
             "• Autonomous AI agents (like AutoGPT, OpenDevin, local Ollama) run tools and execute terminal commands.\n"
             "• If an agent gets prompt-injected or goes rogue, it might try to escape its sandbox (e.g., mounting /var/run/docker.sock to access the host system).\n"
             "• Log Sentry tracks process lineage: if an AI agent runtime spawns an interactive shell (/bin/bash -i) or touches container sockets, Log Sentry flags it immediately as an AI Sandbox Breakout."),

            ("Q4: Who is the target user of this system?",
             "Key Talking Points:\n"
             "• Software Developers & DevOps Engineers: Who frequently install 3rd-party packages and run local containers.\n"
             "• Security Analysts (SOC Tiers 1-2): Who need fast log collection, secret sanitization, and screenshot correlation.\n"
             "• Remote Workers & Enterprise Staff: Who need privacy protection against accidental screen-share leaks during calls.")
        ]),

        ("SECTION 2: ARCHITECTURE & TECHNICAL WORKING", [
            ("Q5: Explain the high-level architecture of your project.",
             "Answer in 4 Layers:\n"
             "1. Telemetry Ingestion Layer: Queries OS-level event streams (macOS Unified Log, Windows Event Logs, and active process tables via psutil).\n"
             "2. Behavioral Sentinel Engine (src/main.py): Analyzes process lineage, Shannon write entropy, and MITRE ATT&CK patterns.\n"
             "3. Call Privacy Shield (src/privacy/call_shield.py): Background daemon checking for video conferencing apps and applying DRM window sharing restrictions.\n"
             "4. GUI & Forensic Dashboard (dashboard.html + src/gui/app.py): Real-time Web console built with Python Flask (locally) and Vercel Edge Serverless (cloud)."),

            ("Q6: How does the system operate without slowing down the computer?",
             "Key Talking Points:\n"
             "• Lightweight Polling & Event-Driven Triggers: Process table checks run on a lightweight background daemon thread every 2 seconds.\n"
             "• No Kernel Driver Bloat: Unlike heavy enterprise agents that inject deep kernel extensions (which can cause Blue Screens of Death like the CrowdStrike incident), Log Sentry works entirely via sanctioned user-space OS APIs.\n"
             "• Targeted Entropy Calculation: Entropy is only computed when high-frequency burst writes occur, avoiding disk I/O bottlenecks."),

            ("Q7: How does the cloud version on Vercel differ from the local desktop daemon?",
             "Key Talking Points:\n"
             "• Local Mode (http://localhost:5050): Runs with full OS privileges in Python. Can read live system logs via 'log show', inspect native process tables, and terminate malicious PIDs (SIGKILL).\n"
             "• Cloud Mode (logssentry.vercel.app): Runs on serverless functions. Designed for interactive threat simulation, file upload triage, and browser-based forensic bundle generation without requiring any local installation.")
        ]),

        ("SECTION 3: DETECTION ALGORITHMS & SECURITY DEEP DIVE", [
            ("Q8: How does Shannon Entropy detect Ransomware?",
             "Key Talking Points:\n"
             "• Normal files (source code, plain text, documents) have ordered data. Their Shannon Entropy is typically between 3.5 and 6.0 bits per byte.\n"
             "• When ransomware encrypts files (using AES or ChaCha20), the resulting ciphertext is mathematically indistinguishable from random noise.\n"
             "• Its entropy spikes above 7.8 bits per byte (max theoretical is 8.0).\n"
             "• When the engine detects a sudden burst of high-entropy file writes combined with backup deletion commands (e.g., 'vssadmin delete shadows'), it flags active ransomware with >90% confidence."),

            ("Q9: What is Process Lineage and why is it important?",
             "Key Talking Points:\n"
             "• Process lineage refers to the Parent-Child relationship of running programs (Parent PID -> Child PID).\n"
             "• Legitimate example: Terminal (zsh) spawning 'git push'.\n"
             "• Malicious example: A PDF reader (Acrobat) or an AI agent runtime (Ollama) spawning '/bin/bash' or 'powershell.exe'.\n"
             "• By checking the parent process, Log Sentry identifies whether an action was authorized by a user or spawned stealthily by an exploit."),

            ("Q10: What are Canary Tripwires in your ransomware module?",
             "Key Talking Points:\n"
             "• Canary files are hidden, bait files placed in common user directories (Documents, Desktop).\n"
             "• Legitimate applications never modify these files.\n"
             "• When automated ransomware begins recursively encrypting folders alphabetically, it hits the canary file first.\n"
             "• The moment the canary is modified or deleted, an early-stage trap triggers, isolating the malicious process before actual personal files are damaged."),

            ("Q11: How do you detect Passive Surveillance and Spyware?",
             "Key Talking Points:\n"
             "• Heuristic Rule 1: Detecting background, non-interactive processes executing silent screenshot utilities (e.g., 'screencapture -x -C' on macOS or PowerShell screen grabs on Windows).\n"
             "• Heuristic Rule 2: Tracking unauthorized read attempts on sensitive local credential stores, such as '~/.ssh/id_rsa' or Chrome SQLite 'Login Data' files from unsanctioned binaries.")
        ]),

        ("SECTION 4: CALL PRIVACY SHIELD & DRM MECHANISM", [
            ("Q12: How does the Call Privacy Shield actually work?",
             "Key Talking Points:\n"
             "• Detection: A background daemon inspects the running process table for video conferencing software (Zoom, Microsoft Teams, Google Meet, FaceTime, Webex, OBS).\n"
             "• Enforcement: On macOS, it invokes native AppKit Cocoa window properties:\n"
             "  [window setSharingType: NSWindowSharingNone (0)];\n"
             "• Result: The user sitting in front of the laptop can see the dashboard normally, but any remote viewer on Zoom or screen-recording software captures 100% black pixels.\n"
             "• Real-world analogy: This is the exact same DRM technology used by Netflix, Apple TV, and banking apps to prevent screen recording."),

            ("Q13: Why is NSWindowSharingNone better than simply closing the window?",
             "Key Talking Points:\n"
             "• Closing or hiding the window interrupts the security engineer's monitoring workflow.\n"
             "• With DRM window sharing, the analyst can keep working, inspecting threat feeds, and writing reports during a team call without accidentally broadcasting sensitive IP addresses or zero-day vulnerabilities to call participants.")
        ]),

        ("SECTION 5: FORENSICS & DATA PRIVACY PIPELINE", [
            ("Q14: What is the 3-Step Forensic Scanner?",
             "Answer in 3 Steps:\n"
             "1. Step 1 (Ingest): Collects system event logs from the host OS (last 2 minutes) or allows incident responders to upload an EVTX/log file.\n"
             "2. Step 2 (Sanitize): Automatically scrubs sensitive secrets (GitHub Personal Access Tokens, AWS Access Keys, Bearer JWTs, SSH private keys) using high-entropy regex filters.\n"
             "3. Step 3 (Evidence Correlation): Accepts pasted/dropped screenshots and synchronizes their visual timestamps with exact kernel log lines."),

            ("Q15: Why is log sanitization critical before forensic analysis?",
             "Key Talking Points:\n"
             "• When developers or SOC analysts export diagnostic logs to share with vendors, third-party SIEMs, or LLMs, logs frequently contain leaked credentials (e.g., 'Authorization: Bearer ...', 'AKIA...').\n"
             "• Sanitizing these strings with safety masks ('[REDACTED_AWS_KEY]') prevents secondary credential leak disasters during incident response.")
        ]),

        ("SECTION 6: CHALLENGES, LIMITATIONS & FUTURE SCOPE", [
            ("Q16: What was the most challenging technical hurdle in this project?",
             "Key Talking Points:\n"
             "• Background Daemon False Positives: On macOS, Apple runs background sync daemons like 'facetimemessagestored' even when FaceTime isn't running. We had to implement exact binary path verification to avoid false call detections.\n"
             "• Cross-Platform Telemetry: Harmonizing telemetry streams between macOS ('log show'), Linux ('/var/log/audit'), and Windows Event Logs into a unified JSON format.\n"
             "• Balancing Accuracy vs. False Alarms: Tuning the Shannon entropy threshold (7.8 bits/byte) so compressed archives (.zip, .mp4) aren't mistakenly classified as ransomware."),

            ("Q17: What are the current limitations of Log Sentry?",
             "Key Talking Points:\n"
             "• User-Space Operation: Because it avoids intrusive kernel drivers, kernel-level rootkits that hook directly into Ring 0 could potentially tamper with process table outputs.\n"
             "• Memory-Only Attacks: Advanced reflective DLL injection that never writes to disk requires dedicated eBPF or memory scraping extensions for 100% coverage."),

            ("Q18: What future enhancements are planned?",
             "Key Talking Points:\n"
             "• eBPF Linux Kernel Probes: Replacing process table polling on Linux with low-overhead eBPF kprobes for zero-overhead syscall interception.\n"
             "• LLM-Powered Natural Language Incident Reports: Integrating local private models to explain attack timelines in plain human English for non-technical executives.\n"
             "• Automated Rollback: Taking instant Volume Shadow snapshots before suspicious file writes to allow 1-click ransomware decryption rollback.")
        ])
    ]

    for section_title, qna_pairs in sections_data:
        h1 = doc.add_heading(level=1)
        r_h1 = h1.add_run(section_title)
        r_h1.font.size = Pt(12)
        r_h1.font.bold = True
        r_h1.font.color.rgb = RGBColor(16, 185, 129)
        h1.paragraph_format.space_before = Pt(14)
        h1.paragraph_format.space_after = Pt(6)

        for q_text, a_text in qna_pairs:
            # Table Card for Q&A
            t = doc.add_table(rows=2, cols=1)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            t.autofit = False

            # Question Cell
            q_cell = t.rows[0].cells[0]
            set_cell_background(q_cell, "0F172A") # Slate 900
            set_cell_margins(q_cell, 80, 80, 140, 140)
            pq = q_cell.paragraphs[0]
            pq.paragraph_format.space_before = Pt(2)
            pq.paragraph_format.space_after = Pt(2)
            rq = pq.add_run(q_text)
            rq.font.bold = True
            rq.font.size = Pt(10)
            rq.font.color.rgb = RGBColor(255, 255, 255)

            # Answer Cell
            a_cell = t.rows[1].cells[0]
            set_cell_background(a_cell, "F8FAFC") # Slate 50
            set_cell_margins(a_cell, 100, 100, 140, 140)
            pa = a_cell.paragraphs[0]
            pa.paragraph_format.space_before = Pt(4)
            pa.paragraph_format.space_after = Pt(4)
            
            # Format answer lines
            lines = a_text.split("\n")
            for i, line in enumerate(lines):
                if i > 0:
                    pa = a_cell.add_paragraph()
                    pa.paragraph_format.space_before = Pt(1)
                    pa.paragraph_format.space_after = Pt(2)

                line_strip = line.strip()
                if line_strip.startswith("•") or line_strip.startswith("1.") or line_strip.startswith("2.") or line_strip.startswith("3.") or line_strip.startswith("4."):
                    # Highlight bold prefixes
                    parts = line_strip.split(":", 1)
                    if len(parts) == 2:
                        r_bld = pa.add_run(parts[0] + ":")
                        r_bld.font.bold = True
                        r_bld.font.size = Pt(9.5)
                        r_bld.font.color.rgb = RGBColor(15, 23, 42)
                        
                        r_rst = pa.add_run(" " + parts[1].strip())
                        r_rst.font.size = Pt(9.5)
                        r_rst.font.color.rgb = RGBColor(51, 65, 85)
                    else:
                        r_rst = pa.add_run(line_strip)
                        r_rst.font.size = Pt(9.5)
                        r_rst.font.color.rgb = RGBColor(51, 65, 85)
                elif "Points" in line or "Steps" in line:
                    r_hd = pa.add_run(line_strip)
                    r_hd.font.bold = True
                    r_hd.font.italic = True
                    r_hd.font.size = Pt(9.5)
                    r_hd.font.color.rgb = RGBColor(16, 185, 129)
                else:
                    r_txt = pa.add_run(line_strip)
                    r_txt.font.size = Pt(9.5)
                    r_txt.font.color.rgb = RGBColor(51, 65, 85)

            # Spacing between cards
            p_space = doc.add_paragraph()
            p_space.paragraph_format.space_before = Pt(0)
            p_space.paragraph_format.space_after = Pt(4)

    doc.save(DOCX_PATH)
    print("Viva Q&A document created at:", DOCX_PATH)

if __name__ == "__main__":
    build_qna_document()
