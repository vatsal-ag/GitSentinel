import zipfile
import tarfile
import os
import subprocess

def package():
    downloads_dir = "src/gui/static/downloads"
    os.makedirs(downloads_dir, exist_ok=True)
    
    # 1. macOS zip
    mac_zip = os.path.join(downloads_dir, "LogSentry-macOS.zip")
    if os.path.exists(mac_zip):
        os.remove(mac_zip)
    subprocess.run(["zip", "-r", "-X", "-q", mac_zip, "LogSentry.app", "-x", "*.DS_Store"], check=True)
    print(f"Built macOS zip: {os.path.getsize(mac_zip)} bytes")

    # 2. Windows zip
    win_zip = os.path.join(downloads_dir, "LogSentry-Windows.zip")
    if os.path.exists(win_zip):
        os.remove(win_zip)
    with zipfile.ZipFile(win_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write('run_app.bat', 'run_app.bat')
        zf.write('requirements.txt', 'requirements.txt')
        zf.write('config/threat_db.json', 'config/threat_db.json')
        zf.write('dashboard.html', 'dashboard.html')
        zf.write('index.html', 'index.html')
        for root, dirs, files in os.walk('src'):
            if 'downloads' in root or '__pycache__' in root:
                continue
            for f in files:
                if f.endswith('.mp4'):
                    continue
                p = os.path.join(root, f)
                zf.write(p, p)
    print(f"Built Windows zip: {os.path.getsize(win_zip)} bytes")

    # 3. Linux tar.gz
    linux_tar = os.path.join(downloads_dir, "LogSentry-Linux.tar.gz")
    if os.path.exists(linux_tar):
        os.remove(linux_tar)
    with tarfile.open(linux_tar, 'w:gz') as tf:
        tf.add('run_app.sh', arcname='run_app.sh')
        tf.add('requirements.txt', arcname='requirements.txt')
        tf.add('config/threat_db.json', arcname='config/threat_db.json')
        tf.add('dashboard.html', arcname='dashboard.html')
        tf.add('index.html', arcname='index.html')
        for root, dirs, files in os.walk('src'):
            if 'downloads' in root or '__pycache__' in root:
                continue
            for f in files:
                if f.endswith('.mp4'):
                    continue
                p = os.path.join(root, f)
                tf.add(p, arcname=p)
    print(f"Built Linux tar.gz: {os.path.getsize(linux_tar)} bytes")

if __name__ == "__main__":
    package()
