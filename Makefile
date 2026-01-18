# Makefile für S&P 500 GARCH Volatilitätsanalyse
# Verwendung: make <target>

.PHONY: help install run clean

# Default target
help:
	@echo "S&P 500 GARCH Volatilitätsanalyse - Verfügbare Befehle:"
	@echo ""
	@echo "  make install        - Installiert alle Abhängigkeiten"
	@echo "  make run            - Startet Jupyter Notebook"
	@echo "  make clean          - Entfernt generierte Dateien"
	@echo ""

# Python-Umgebung einrichten
venv:
	python3 -m venv venv
	@echo "✅ Virtuelle Umgebung erstellt"
	@echo "Aktivieren mit: source venv/bin/activate"

# Abhängigkeiten installieren
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Abhängigkeiten installiert"

# Jupyter Notebook starten
run:
	jupyter notebook notebooks/garch_analysis_index_erweitert.ipynb

# Aufräumen
clean:
	@echo "🧹 Räume auf..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .pytest_cache .ipynb_checkpoints
	@echo "✅ Aufräumen abgeschlossen"

# Projekt-Übersicht
info:
	@echo "📊 S&P 500 GARCH Volatilitätsanalyse"
	@echo "Version: 1.0.0"
	@echo "Python: $$(python --version)"
	@echo "Pip: $$(pip --version)"
	@echo ""
	@echo "Verzeichnisstruktur:"
	@tree -L 2 -I 'venv|__pycache__|*.egg-info' || ls -R
