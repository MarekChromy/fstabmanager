🚀 FSTAB Manager PRO
Moderní, lehké a bezpečné webové rozhraní pro správu souboru /etc/fstab v systémech Linux (optimalizováno pro KDE Plasma). Už žádné ruční upravování konfiguračních souborů v terminálu a strach z chyb v syntaxi.

✨ Funkce
Pohodlná správa: Přidávání a mazání přípojných bodů (disků) přes čisté webové UI.

Bezpečnost na prvním místě: Automatická integrace s pkexec pro grafické vyžádání hesla roota.

Systémová kontrola: Přímý výhled na lsblk (seznam disků) a surový obsah fstab přímo v aplikaci.

Aplikace změn: Tlačítko pro mount -a a daemon-reload, které okamžitě aktivuje provedené změny.

Ultra-Wide Design: Moderní tmavý vzhled, který využívá celou šířku monitoru a je skvěle čitelný.

Auto-Open: Po spuštění z Dolphinu nebo konzole se automaticky otevře tvůj výchozí prohlížeč.

🛠️ Instalace a spuštění
1. Prerekvizity
Aplikace vyžaduje Python 3 a knihovnu Flask. Nainstaluješ ji snadno:

Bash
sudo apt update
sudo apt install python3-flask
2. Stažení
Ulož skript fstab_manager.py do svého domovského adresáře.

3. Spuštění z terminálu
Bash
python3 fstab_manager.py
4. Nastavení pro Dolphin (KDE)
Aby se aplikace spouštěla na jedno kliknutí přímo ze správce souborů:

Klikni na fstab_manager.py pravým tlačítkem.

Vyber Vlastnosti -> Oprávnění.

Zaškrtni Je spustitelný.

Nyní stačí na soubor kliknout a zvolit Spustit.

🖥️ Technologie
Backend: Python 3 + Flask

Frontend: HTML5, CSS3 (Modern Dark Theme), FontAwesome 6

Systém: Linux (testováno na KDE Plasma, Debian/Ubuntu/Kubuntu)

⚠️ Varování
Úprava souboru /etc/fstab je kritická operace. Před aplikací změn se ujistěte, že zadané UUID nebo cesty k diskům jsou správné. Aplikace automaticky vytváří přípojné body (složky), pokud neexistují.
