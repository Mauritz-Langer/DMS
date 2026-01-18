# Notebooks - Jupyter Notebooks für die Analyse

## 📓 Übersicht

Dieser Ordner enthält alle Jupyter Notebooks für die S&P 500 GARCH Volatilitätsanalyse.

## 📚 Notebooks

### GARCH_Analyse.ipynb

**Hauptanalyse-Notebook** - Umfassende GARCH-Volatilitätsprognose des S&P 500

#### Inhalt

0. **Installation und Abhängigkeiten** - Setup-Anweisungen
1. **Deskriptive Analyse** - S&P 500 Einzelaktiendaten
2. **Index-Daten laden** - S&P 500 Index und Renditen
3. **Stationaritätstest** - ADF-Test (Augmented Dickey-Fuller)
4. **GARCH-Modellierung** - GARCH(1,1), EGARCH, GJR-GARCH
5. **Out-of-Sample Prognose** - Rolling Forecast
6. **Modellevaluation** - MSE/MAE-Vergleich
7. **Leverage-Effekt** - Visualisierung asymmetrischer Reaktionen
8. **Konfidenzintervalle** - Unsicherheitsbereiche
9. **Zusammenfassung** - Fazit und Empfehlungen

#### Ausführung

```bash
# Terminal
cd /Users/mauritzlanger/Programmierung/DMS
jupyter notebook notebooks/GARCH_Analyse.ipynb

# Oder mit Makefile
make run
```

#### Wichtige Outputs

Das Notebook generiert:
- **Grafiken** → `output/figures/`
  - Zeitreihen der Renditen
  - Volatilitätscluster
  - Modellvergleiche
  - Leverage-Effekt-Diagramme
  - Prognose mit Konfidenzintervallen

- **Ergebnisse** → `output/results/`
  - MSE/MAE-Tabellen
  - Modellparameter
  - Statistische Tests

#### Geschätzte Laufzeit

- **Vollständige Ausführung:** 5-10 Minuten (je nach System)
- **Einzelne Abschnitte:** 30 Sekunden - 2 Minuten

#### Voraussetzungen

```bash
pip install -r requirements.txt
```

Siehe [requirements.txt](../requirements.txt) für Details.

## 🔧 Notebook-Entwicklung

### Best Practices

1. **Kernel neustarten** nach großen Änderungen
   ```
   Kernel → Restart & Clear Output
   ```

2. **Regelmäßig speichern** (`Cmd + S` / `Strg + S`)

3. **Outputs clearen** vor Git-Commits
   ```bash
   jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
   ```

4. **Zellen in logische Abschnitte** unterteilen

5. **Markdown-Zellen** für Dokumentation nutzen

### Fehlerbehebung

#### "Kernel died"
- Zu wenig RAM → Reduzieren Sie die Datenmenge oder schließen Sie andere Programme
- Inkompatible Pakete → Neuinstallation: `pip install --force-reinstall arch`

#### "ModuleNotFoundError"
```bash
# Stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist
source venv/bin/activate
pip install -r requirements.txt
```

#### Langsame Ausführung
- Rolling Forecast kann zeitintensiv sein → Reduzieren Sie `WINDOW_SIZE` in Tests
- Schließen Sie nicht benötigte Browser-Tabs

## 📊 Erweiterungen

Mögliche zukünftige Notebooks:

- `garch_individual_stocks.ipynb` - Analyse einzelner S&P 500 Aktien
- `model_comparison_extended.ipynb` - Weitere Modelle (FIGARCH, IGARCH)
- `crisis_analysis.ipynb` - Vertiefende Analyse von Finanzkrisen
- `portfolio_optimization.ipynb` - GARCH-basierte Portfoliostrategien

## 📖 Weitere Ressourcen

- [Jupyter Notebook Dokumentation](https://jupyter-notebook.readthedocs.io/)
- [ARCH Package Dokumentation](https://arch.readthedocs.io/)
- [Pandas Cheatsheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

## 🆘 Hilfe

Bei Fragen oder Problemen:
1. Konsultieren Sie [QUICKSTART.md](../QUICKSTART.md)
2. Prüfen Sie [CONTRIBUTING.md](../CONTRIBUTING.md)
3. Öffnen Sie ein Issue im Repository

---

**Happy Analyzing!** 📈
