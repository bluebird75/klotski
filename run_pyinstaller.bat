pyinstaller run_klotski.py ^
    --noconfirm ^
	--add-data src\boards.kts;. ^
	--add-binary src\klotski-icon.png;. ^
	--add-binary src\klotski-tiles.png;. ^
	--onefile --windowed --icon src\klotski-icon.ico
	