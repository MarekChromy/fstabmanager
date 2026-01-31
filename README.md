
# 🚀 FSTAB Manager PRO

Moderní, lehké a bezpečné webové rozhraní pro správu systémového souboru `/etc/fstab` v Linuxu. Navrženo speciálně pro uživatele KDE Plasma (Dolphin), ale plně funkční v jakémkoliv distribuci.

!

## ✨ Hlavní funkce

- **Správa v reálném čase:** Přidávání, odebírání a úprava přípojných bodů disků přes webové UI.
- **Bezpečné oprávnění:** Automatická integrace s `pkexec` (PolicyKit) – skript si sám vyžádá heslo roota v grafickém okně.
- **Inteligentní otevírání:** Při spuštění z Dolphinu se automaticky identifikuje uživatel a otevře se prohlížeč v jeho seanci.
- **Systémová diagnostika:** Integrovaný výpis `lsblk -f` pro snadné kopírování UUID a kontrolu disků.
- **Aplikace změn:** Možnost provést `systemctl daemon-reload` a `mount -a` přímo z prohlížeče.
- **Ultra-Wide Design:** Tmavé téma (Dark Mode) optimalizované pro širokoúhlé monitory s důrazem na čitelnost.

## 🛠️ Instalace

Aplikace vyžaduje Python 3 a knihovnu Flask.

```bash
# Instalace na Debian/Ubuntu/Kubuntu:
sudo apt update
sudo apt install python3-flask

# Instalace na Arch Linux:
sudo pacman -S python-flask

# Instalace na Fedora:
sudo dnf install python3-flask
🚀 Jak používat
Spuštění z terminálu
Bash
python3 fstab_manager.py
Spuštění z Dolphinu (KDE)
Klikněte pravým tlačítkem na fstab_manager.py.

Zvolte Vlastnosti -> Oprávnění.

Zaškrtněte Je spustitelný (Is executable).

Napříště stačí na soubor poklepat a zvolit Spustit.

🖥️ Náhled rozhraní
Aplikace běží lokálně na portu 5005 (nebo prvním volném). Rozhraní je rozděleno do tří hlavních sekcí pod sebou:

Tabulka fstab: Aktuálně zavedené disky s možností smazání.

lsblk: Seznam všech fyzických disků a jejich UUID pro snadné vkládání.

Raw fstab: Surový náhled textového souboru pro kontrolu.

⚠️ Důležité upozornění
Soubor /etc/fstab je kritickou součástí systému.

Před smazáním řádku se ujistěte, že nejde o systémový oddíl (root / nebo /boot).

Aplikace při přidávání disku automaticky vytvoří cílovou složku (mountpoint), pokud ještě neexistuje.

📄 Licence
Tento projekt je open-source. Upravujte a šiřte dle libosti.
Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
Nevybrán žádný soubor
Attach files by dragging & dropping, selecting or pasting them.
