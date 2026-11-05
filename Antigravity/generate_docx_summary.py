import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

os.makedirs("Antigravity", exist_ok=True)
CHART_PATH = "Antigravity/flowchart.png"
DOCX_PATH = "Log_Sentry_EDR_Architecture.docx"

def generate_flowchart():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    
    # Coordinates and dimensions
    # 4 columns/tiers
    # Col 1: Ingestion (x=0.5)
    # Col 2: Analysis (x=3.8)
    # Col 3: Actions / Privacy (x=7.2)
    # Col 4: Presentation / Forensic (x=10.5)
    
    # We will draw a top-down / left-to-right modern system flow
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Helper to draw boxes
    def draw_card(x, y, w, h, title, subtitle, bg_color='#f8fafc', border_color='#cbd5e1', title_color='#0f172a', sub_color='#475569'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.15",
                                      linewidth=1.5, edgecolor=border_color, facecolor=bg_color)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.65, title, fontsize=9.5, fontweight='bold', color=title_color, ha='center', va='center')
        ax.text(x + w/2, y + h*0.28, subtitle, fontsize=7.5, color=sub_color, ha='center', va='center')

    # Draw Stage Headers
    headers = [
        ("1. INGESTION", 1.8),
        ("2. DETECTION ENGINE", 5.2),
        ("3. ENFORCEMENT & PRIVACY", 8.4),
        ("4. FORENSICS & GUI", 11.0)
    ]
    for text, cx in headers:
        ax.text(cx, 8.1, text, fontsize=9, fontweight='heavy', color='#059669', ha='center', va='center')

    # Column 1: Ingestion
    draw_card(0.4, 6.2, 2.7, 1.2, "Host OS Telemetry", "Process Trees • Syscalls • File I/O", bg_color='#ecfdf5', border_color='#10b981')
    draw_card(0.4, 4.4, 2.7, 1.2, "Meeting Monitor Daemon", "Zoom • Teams • Meet • FaceTime", bg_color='#eff6ff', border_color='#3b82f6')
    draw_card(0.4, 2.6, 2.7, 1.2, "Audit Log Streams", "macOS log show • Windows Events", bg_color='#f8fafc', border_color='#94a3b8')

    # Column 2: Detection Engine
    draw_card(3.8, 6.2, 2.8, 1.2, "Shannon Entropy Sensor", "Write bursts > 7.8 bits/byte", bg_color='#ecfdf5', border_color='#10b981')
    draw_card(3.8, 4.4, 2.8, 1.2, "Process Lineage & Escape", "docker.sock • Agent Breakouts", bg_color='#fef2f2', border_color='#ef4444')
    draw_card(3.8, 2.6, 2.8, 1.2, "Spyware & Keylog Hunter", "Silent Screengrab • SSH theft", bg_color='#fefce8', border_color='#eab308')

    # Column 3: Enforcement & Privacy
    draw_card(7.1, 6.2, 2.6, 1.2, "Process Quarantine", "Instant PID Kill (SIGKILL)", bg_color='#fef2f2', border_color='#ef4444')
    draw_card(7.1, 4.4, 2.6, 1.2, "DRM Screen Blackout", "NSWindowSharingNone (0)", bg_color='#eff6ff', border_color='#3b82f6')
    draw_card(7.1, 2.6, 2.6, 1.2, "Secret Redaction Engine", "Scrubs GitHub PATs & AWS keys", bg_color='#f8fafc', border_color='#64748b')

    # Column 4: Forensics & Output
    draw_card(10.1, 5.3, 1.7, 2.1, "Web GUI\nDashboard", "Live Feed • SOC\nTelemetry • Alerts", bg_color='#ecfdf5', border_color='#10b981')
    draw_card(10.1, 2.6, 1.7, 1.2, "Forensic Bundle", "Screenshot & Log Sync", bg_color='#f8fafc', border_color='#94a3b8')

    # Connectors (Arrows)
    def arrow(x1, y1, x2, y2, color='#64748b', style='->', lw=1.5):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=3, shrinkB=3))

    # Flow 1: Telemetry -> Sensors
    arrow(3.1, 6.8, 3.8, 6.8, '#10b981')
    arrow(3.1, 6.8, 3.8, 5.0, '#ef4444')
    arrow(3.1, 6.8, 3.8, 3.2, '#eab308')

    # Flow 2: Meeting monitor -> DRM Blackout
    arrow(3.1, 5.0, 7.1, 5.0, '#3b82f6', lw=2)

    # Flow 3: Audit Logs -> Secret Redaction
    arrow(3.1, 3.2, 7.1, 3.2, '#64748b')

    # Flow 4: Threats -> Quarantine & Alerts
    arrow(6.6, 6.8, 7.1, 6.8, '#ef4444')
    arrow(6.6, 5.0, 7.1, 6.8, '#ef4444')
    arrow(6.6, 3.2, 7.1, 6.8, '#ef4444')

    # Flow 5: Actions -> Dashboard & Bundles
    arrow(9.7, 6.8, 10.1, 6.4, '#10b981')
    arrow(9.7, 5.0, 10.1, 5.8, '#3b82f6')
    arrow(9.7, 3.2, 10.1, 3.2, '#64748b')
    arrow(10.9, 3.8, 10.9, 5.3, '#94a3b8', style='<->')

    # Add Legend Banner at bottom
    ax.text(6.0, 0.9, "Log Sentry EDR Telemetry & DRM Privacy Lifecycle — Closed Loop Protection", 
            fontsize=8.5, fontweight='bold', color='#475569', ha='center', va='center')
    ax.text(6.0, 0.45, "Behavioral Heuristics • Zero-Day / AI Breakout Detection • Netflix-Grade DRM Screen Obfuscation",
            fontsize=7.5, color='#94a3b8', ha='center', va='center')

    plt.tight_layout()
    plt.savefig(CHART_PATH, bbox_inches='tight', facecolor='#ffffff')
    plt.close()
    print("Flowchart generated at:", CHART_PATH)

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

def create_docx():
    doc = Document()
    
    # Set standard margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # Styles helper
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # Header / Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_badge = p_title.add_run("BEHAVIORAL ENDPOINT DETECTION & RESPONSE\n")
    run_badge.font.size = Pt(9)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green

    run_title = p_title.add_run("Log Sentry EDR: Architecture & Working Guide")
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Executive operational walkthrough of the behavioral engine, DRM privacy curtain, and forensic triage pipeline.")
    run_sub.font.size = Pt(10)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # 1. Executive Summary
    h1 = doc.add_heading(level=1)
    run_h1 = h1.add_run("1. Executive Summary")
    run_h1.font.size = Pt(13)
    run_h1.font.bold = True
    run_h1.font.color.rgb = RGBColor(15, 23, 42)
    h1.paragraph_format.space_after = Pt(6)

    bullets = [
        ("Behavioral, Not Hash-Based: ", "Detects polymorphic malware, zero-days, and AI breakouts via live OS entropy and process lineage, completely bypassing evasion techniques."),
        ("DRM Screen Privacy Shield: ", "Detects active meeting software (FaceTime, Zoom, Teams, Meet) and sets native AppKit NSWindowSharingNone to black out screenshares."),
        ("Automated Forensics & Sanitization: ", "Redacts credentials (GitHub PATs, AWS keys, JWTs) before correlating screenshots with kernel event logs.")
    ]
    for b_title, b_desc in bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(3)
        r_bt = p_b.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.color.rgb = RGBColor(16, 185, 129)
        r_bd = p_b.add_run(b_desc)

    # 2. System Flowchart
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    h2 = doc.add_heading(level=1)
    run_h2 = h2.add_run("2. System Architecture Flowchart")
    run_h2.font.size = Pt(13)
    run_h2.font.bold = True
    run_h2.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_after = Pt(6)

    # Add the Flowchart Image
    if os.path.exists(CHART_PATH):
        doc.add_picture(CHART_PATH, width=Inches(6.8))
        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_before = Pt(4)
        p_caption.paragraph_format.space_after = Pt(12)
        r_cap = p_caption.add_run("Figure 1: End-to-end telemetry lifecycle from kernel monitoring to DRM enforcement and web GUI.")
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(148, 163, 184)

    # 3. Core Working Modules
    h3 = doc.add_heading(level=1)
    run_h3 = h3.add_run("3. Core Working Modules")
    run_h3.font.size = Pt(13)
    run_h3.font.bold = True
    run_h3.font.color.rgb = RGBColor(15, 23, 42)
    h3.paragraph_format.space_after = Pt(6)

    modules = [
        ("A. Sentinel Behavioral Engine (src/main.py)",
         "• Shannon Entropy Check: Computes write-entropy. Spikes above 7.8 bits/byte combined with backup deletion indicate active ransomware.\n"
         "• AI Sandbox Breakouts: Flags interactive shells spawned by local agent runtimes (Ollama/AutoGPT) targeting /var/run/docker.sock.\n"
         "• Passive Surveillance: Tracks silent screencapture commands and unauthorized credential store access."),
        
        ("B. Call Privacy Shield & DRM Blackout (src/privacy/call_shield.py)",
         "• Process Monitor Daemon: Background thread continuously checks process tables for Zoom, Teams, Meet, FaceTime, and OBS.\n"
         "• macOS AppKit DRM: Calls [window setSharingType:NSWindowSharingNone (0)]. Content renders normally on the host display while broadcasting 100% black pixels on conference streams.\n"
         "• Blackout Curtain UI: Immediately overlays sensitive dashboards during screen-sharing events."),

        ("C. Forensic Pipeline & Log Sanitizer (src/privacy/log_sanitizer.py)",
         "• Ingest: Pulls the last 2 minutes of OS logs or loads incident benchmark samples.\n"
         "• Sanitize: RegEx entropy engines scrub GitHub tokens, AWS keys, JWTs, and private keys.\n"
         "• Correlate: Synchronizes user-uploaded incident screenshots with millisecond-precision log timestamps."),

        ("D. Hybrid Operating Stack (Local Daemon vs. Cloud Web)",
         "• Local Mode: Python 3 Flask daemon (http://localhost:5050) interacting directly with kernel APIs.\n"
         "• Cloud Mode (logssentry.vercel.app): Edge serverless functions with autonomous browser-side simulation fallback.")
    ]

    for m_title, m_desc in modules:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_before = Pt(4)
        p_m.paragraph_format.space_after = Pt(2)
        r_mt = p_m.add_run(m_title)
        r_mt.font.bold = True
        r_mt.font.size = Pt(11)
        r_mt.font.color.rgb = RGBColor(16, 185, 129)

        p_md = doc.add_paragraph()
        p_md.paragraph_format.space_after = Pt(6)
        r_md = p_md.add_run(m_desc)
        r_md.font.size = Pt(10)

    # 4. Threat Detection Matrix
    h4 = doc.add_heading(level=1)
    run_h4 = h4.add_run("4. Threat Detection Matrix")
    run_h4.font.size = Pt(13)
    run_h4.font.bold = True
    run_h4.font.color.rgb = RGBColor(15, 23, 42)
    h4.paragraph_format.space_after = Pt(6)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ["Threat Category", "Detection Method", "MITRE ATT&CK", "Automated Action"]
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "10B981")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Ransomware (WannaCry)", "File entropy > 7.8 + shadow deletion", "T1486 (Data Encrypted)", "Instant SIGKILL + Rollback"),
        ("AI Agent Breakout", "Lineage check on /var/run/docker.sock", "T1611 (Escape to Host)", "Quarantine container socket"),
        ("Passive Surveillance", "Background screencapture / sqlite3 query", "T1113 (Screen Capture)", "Terminate child process"),
        ("Screen Privacy Leak", "Active Zoom / Teams / FaceTime stream", "N/A (Data Loss Prevention)", "Deploy DRM NSWindowSharingNone")
    ]

    for cat, method, mitre, action in data:
        row = table.add_row()
        cells = row.cells
        cells[0].text = cat
        cells[1].text = method
        cells[2].text = mitre
        cells[3].text = action

        for j, cell in enumerate(cells):
            set_cell_background(cell, "F8FAFC" if j % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            for r in p.runs:
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(DOCX_PATH)
    print("Docx created successfully at:", DOCX_PATH)

if __name__ == "__main__":
    generate_flowchart()
    create_docx()
