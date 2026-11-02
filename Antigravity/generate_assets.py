import os
from PIL import Image, ImageDraw, ImageFont

def generate_assets():
    static_dir = "src/gui/static"
    os.makedirs(static_dir, exist_ok=True)
    
    # 1. Vector icon.svg
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <rect width="100" height="100" rx="22" fill="#09090b"/>
  <rect x="1" y="1" width="98" height="98" rx="21" stroke="#27272a" stroke-width="2"/>
  <!-- Shield Path -->
  <path d="M50 16L78 28V48C78 66 66 81 50 86C34 81 22 66 22 48V28L50 16Z" fill="#121215" stroke="url(#shieldGrad)" stroke-width="3" filter="url(#glow)"/>
  <!-- Checkmark / Pulse Radar -->
  <path d="M38 48L46 56L62 38" stroke="#10b981" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Center Core Dot -->
  <circle cx="50" cy="72" r="2.5" fill="#34d399"/>
</svg>'''
    with open("icon.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    with open(os.path.join(static_dir, "icon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("✓ Created icon.svg")

    # 2. Base High-Res Icon (512x512)
    img_512 = Image.new("RGBA", (512, 512), (9, 9, 11, 255))
    draw = ImageDraw.Draw(img_512)
    # Border
    draw.rounded_rectangle([4, 4, 508, 508], radius=110, outline=(39, 39, 42, 255), width=6)
    # Outer Shield
    shield_pts = [
        (256, 80),
        (400, 140),
        (400, 245),
        (256, 440),
        (112, 245),
        (112, 140)
    ]
    draw.polygon(shield_pts, fill=(18, 18, 21, 255), outline=(16, 185, 129, 255))
    # Inner Accent Lines
    draw.line([(195, 245), (235, 285), (320, 195)], fill=(16, 185, 129, 255), width=18)
    draw.ellipse([(246, 365), (266, 385)], fill=(52, 211, 153, 255))

    # Save apple-touch-icon.png (180x180)
    img_180 = img_512.resize((180, 180), Image.Resampling.LANCZOS)
    img_180.save("apple-touch-icon.png", format="PNG")
    img_180.save(os.path.join(static_dir, "apple-touch-icon.png"), format="PNG")
    print("✓ Created apple-touch-icon.png (180x180)")

    # Save favicon.ico (16, 32, 48)
    img_512.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    img_512.save(os.path.join(static_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("✓ Created favicon.ico")

    # 3. High-Resolution OG Social Card (1200x630)
    og = Image.new("RGBA", (1200, 630), (9, 9, 11, 255))
    og_draw = ImageDraw.Draw(og)
    
    # Outer border
    og_draw.rectangle([0, 0, 1199, 629], outline=(39, 39, 42, 255), width=2)
    # Top Accent Line
    og_draw.line([(0, 0), (1200, 0)], fill=(16, 185, 129, 255), width=4)

    # Grid Lines background effect (faint zinc)
    for x in range(40, 1200, 80):
        og_draw.line([(x, 0), (x, 630)], fill=(24, 24, 27, 120), width=1)
    for y in range(40, 630, 80):
        og_draw.line([(0, y), (1200, y)], fill=(24, 24, 27, 120), width=1)

    # Card Panel Container
    og_draw.rounded_rectangle([60, 60, 1140, 570], radius=20, fill=(18, 18, 21, 235), outline=(16, 185, 129, 80), width=2)

    # Paste shield logo on left
    logo_thumb = img_512.resize((160, 160), Image.Resampling.LANCZOS)
    og.paste(logo_thumb, (110, 120), logo_thumb)

    # Try default fonts or system font
    try:
        font_headline = ImageFont.truetype("/System/Library/Fonts/SFPro-Bold.otf", 54)
        font_sub = ImageFont.truetype("/System/Library/Fonts/SFPro-Regular.otf", 26)
        font_tag = ImageFont.truetype("/System/Library/Fonts/SFPro-Medium.otf", 20)
        font_mono = ImageFont.truetype("/System/Library/Fonts/SFMono-Bold.otf", 20)
    except Exception:
        font_headline = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_mono = ImageFont.load_default()

    # Draw Title & Copy
    og_draw.text((310, 130), "LOG SENTRY", fill=(250, 250, 250, 255), font=font_headline)
    og_draw.rounded_rectangle([670, 138, 800, 178], radius=6, fill=(16, 185, 129, 35), outline=(16, 185, 129, 120), width=1)
    og_draw.text((685, 146), "EDR 2.0", fill=(16, 185, 129, 255), font=font_mono)

    og_draw.text((310, 200), "Universal Behavioral EDR & Supply-Chain Defense", fill=(16, 185, 129, 255), font=font_sub)
    og_draw.text((110, 320), "• AI Sandbox Escape Detection (Docker Socket Hijacks, Container Escapes)", fill=(228, 228, 231, 255), font=font_sub)
    og_draw.text((110, 365), "• Ransomware Defense (Volume Shadow Deletions, Canary Integrity)", fill=(228, 228, 231, 255), font=font_sub)
    og_draw.text((110, 410), "• Anti-Screen Sharing Call Privacy Shield (Netflix-Grade DRM Blackout)", fill=(228, 228, 231, 255), font=font_sub)
    og_draw.text((110, 455), "• Cross-Platform Telemetry: macOS os_log • Windows Sysmon • Linux auditd", fill=(161, 161, 170, 255), font=font_sub)

    # Footer metrics bar
    og_draw.rounded_rectangle([110, 500, 1090, 545], radius=8, fill=(9, 9, 11, 255), outline=(39, 39, 42, 255), width=1)
    og_draw.text((130, 513), "ZERO KERNEL EXTENSIONS  |  LOCAL-FIRST FORENSICS  |  OPEN-SOURCE EDR", fill=(16, 185, 129, 255), font=font_mono)
    og_draw.text((920, 513), "logsentry.io", fill=(161, 161, 170, 255), font=font_mono)

    og.save("og-image.png", format="PNG")
    og.save(os.path.join(static_dir, "og-image.png"), format="PNG")
    print("✓ Created og-image.png (1200x630 high resolution card)")

if __name__ == "__main__":
    generate_assets()
