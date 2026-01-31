#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import threading
import time
import socket
from pathlib import Path
from dataclasses import dataclass
from flask import Flask, request, render_template_string, flash, redirect, url_for

# --- GRAFICKÉ PŘIHLÁŠENÍ ---
if os.geteuid() != 0:
    try:
        subprocess.run(['pkexec', sys.executable, *sys.argv], check=True)
        sys.exit(0)
    except:
        sys.exit(1)

app = Flask(__name__)
app.secret_key = 'fstab-manager-ultra-wide-v3'
FSTAB_PATH = "/etc/fstab"

@dataclass
class FstabEntry:
    id: int
    fs_spec: str
    mountpoint: str
    vfstype: str
    options: str

# --- HTML ŠABLONA ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>FSTAB Manager PRO</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --bg: #0F172A; --card: #1E293B; --text: #F8FAFC; --accent: #3B82F6; --success: #10B981; --border: #334155; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; font-size: 1.05rem; line-height: 1.6; }
        .container { width: 95%; margin: 0 auto; padding: 2rem 0; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; border-bottom: 3px solid var(--accent); padding-bottom: 1rem; }
        .card { background: var(--card); border-radius: 12px; padding: 1.5rem; border: 1px solid var(--border); margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 100%; box-sizing: border-box; }
        h3 { margin: 0 0 1.2rem 0; font-size: 1.2rem; color: #94A3B8; display: flex; align-items: center; gap: 10px; }
        .table { width: 100%; border-collapse: collapse; }
        .table th { text-align: left; padding: 12px; color: #64748B; border-bottom: 2px solid var(--border); }
        .table td { padding: 12px; border-bottom: 1px solid var(--border); }
        .btn { padding: 0.7rem 1.3rem; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 8px; color: white; text-decoration: none; }
        .btn-apply { background: var(--success); }
        .btn-primary { background: var(--accent); }
        .btn-danger { background: #EF4444; }
        .btn-sec { background: #475569; }
        pre { background: #000; padding: 1.5rem; border-radius: 10px; color: #10B981; font-size: 0.95rem; overflow-x: auto; margin: 0; border: 1px solid var(--border); width: 100%; box-sizing: border-box; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); align-items: center; justify-content: center; z-index: 1000; }
        .modal.active { display: flex; }
        .modal-content { background: var(--card); padding: 2.5rem; border-radius: 15px; width: 500px; border: 1px solid var(--accent); }
        .form-control { width: 100%; padding: 0.8rem; background: #0F172A; border: 1px solid var(--border); border-radius: 6px; color: white; margin-top: 5px; font-size: 1rem; box-sizing: border-box; }
        .form-group { margin-bottom: 1.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="font-size: 2rem; margin:0;"><i class="fas fa-hdd"></i> FSTAB Manager PRO</h1>
            <div style="display: flex; gap: 15px;">
                <form method="POST"><input type="hidden" name="action" value="apply"><button class="btn btn-apply"><i class="fas fa-save"></i> APLIKOVAT ZMĚNY</button></form>
                <button class="btn btn-primary" onclick="document.getElementById('addM').classList.add('active')"><i class="fas fa-plus-circle"></i> PŘIDAT DISK</button>
                <a href="/shutdown" class="btn btn-sec"><i class="fas fa-power-off"></i></a>
            </div>
        </div>
        {% with msgs = get_flashed_messages() %}{% if msgs %}{% for m in msgs %}
            <div style="background:rgba(59,130,246,0.1); color:#60A5FA; padding:15px; border-radius:8px; margin-bottom:2rem; border:1px solid #3B82F6;">{{ m }}</div>
        {% endfor %}{% endif %}{% endwith %}
        <div class="card">
            <h3><i class="fas fa-list"></i> Konfigurace /etc/fstab</h3>
            <table class="table">
                <thead><tr><th>Zdroj</th><th>Mountpoint</th><th>Typ</th><th>Parametry</th><th style="text-align:right">Akce</th></tr></thead>
                <tbody>
                    {% for e in entries %}
                    <tr>
                        <td><code>{{ e.fs_spec }}</code></td>
                        <td><strong>{{ e.mountpoint }}</strong></td>
                        <td>{{ e.vfstype }}</td>
                        <td>{{ e.options }}</td>
                        <td style="text-align:right">
                            <form method="POST" style="display:inline"><input type="hidden" name="action" value="del"><input type="hidden" name="idx" value="{{ e.id }}">
                            <button class="btn btn-danger" onclick="return confirm('Smazat?')"><i class="fas fa-trash-alt"></i></button></form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="card"><h3><i class="fas fa-microchip"></i> lsblk</h3><pre>{{ lsblk }}</pre></div>
        <div class="card"><h3><i class="fas fa-file-code"></i> fstab raw</h3><pre>{{ raw }}</pre></div>
    </div>
    <div id="addM" class="modal"><div class="modal-content">
        <h2>Nový disk</h2>
        <form method="POST"><input type="hidden" name="action" value="add">
            <div class="form-group"><label>UUID/Cesta</label><input name="spec" class="form-control" required></div>
            <div class="form-group"><label>Mountpoint</label><input name="mnt" class="form-control" required></div>
            <div class="form-group"><label>Typ</label><input name="typ" class="form-control" value="ext4"></div>
            <div class="form-group"><label>Options</label><input name="opt" class="form-control" value="defaults,nofail"></div>
            <button type="submit" class="btn btn-primary">ULOŽIT</button>
            <button type="button" class="btn btn-sec" onclick="document.getElementById('addM').classList.remove('active')">ZRUŠIT</button>
        </form>
    </div></div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        act = request.form.get('action')
        if act == 'add':
            p = Path(request.form['mnt'])
            if not p.exists(): p.mkdir(parents=True, exist_ok=True)
            with open(FSTAB_PATH, 'a') as f:
                f.write(f"\n# Added\n{request.form['spec']} {request.form['mnt']} {request.form['typ']} {request.form['opt']} 0 2\n")
            flash("Záznam přidán.")
        elif act == 'del':
            idx = int(request.form['idx'])
            lines = open(FSTAB_PATH).readlines()
            with open(FSTAB_PATH, 'w') as f:
                for i, l in enumerate(lines):
                    if i != idx: f.write(l)
            flash("Záznam odstraněn.")
        elif act == 'apply':
            subprocess.run(['systemctl', 'daemon-reload'])
            res = subprocess.run(['mount', '-a'], capture_output=True, text=True)
            flash("Změny aplikovány." if res.returncode == 0 else f"Chyba: {res.stderr}")
        return redirect('/')

    entries = []
    if os.path.exists(FSTAB_PATH):
        with open(FSTAB_PATH, 'r') as f:
            for idx, line in enumerate(f):
                p = line.strip().split()
                if p and not line.startswith('#') and len(p) >= 4:
                    entries.append(FstabEntry(idx, p[0], p[1], p[2], p[3]))
    lsblk = subprocess.run(['lsblk', '-f', '-o', 'NAME,FSTYPE,LABEL,UUID,MOUNTPOINT'], capture_output=True, text=True).stdout
    raw = open(FSTAB_PATH).read()
    return render_template_string(HTML_TEMPLATE, entries=entries, lsblk=lsblk, raw=raw)

@app.route('/shutdown')
def shutdown():
    os._exit(0)

def auto_open(port):
    time.sleep(2)
    url = f"http://127.0.0.1:{port}"
    user = os.environ.get('SUDO_USER') or os.environ.get('USER') or "marek"
    # Pokus o otevření prohlížeče v grafickém prostředí uživatele
    env = f"DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/$(id -u {user})"
    cmd = f"su {user} -c '{env} xdg-open {url}'"
    subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

if __name__ == '__main__':
    def get_port():
        p = 5005
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', p)) != 0: return p
                p += 1
    p = get_port()
    threading.Thread(target=auto_open, args=(p,), daemon=True).start()
    app.run(host='127.0.0.1', port=p, debug=False)
