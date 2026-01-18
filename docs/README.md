# Dokumentation - S&P 500 GARCH Volatilitätsanalyse

## 📄 Inhalt

Dieser Ordner enthält die Projektdokumentation und zugehörige Materialien.

### Dateien

- **DMS_Plakat** - Wissenschaftliches Poster für die DMS Präsentation

## 📊 Poster-Übersicht

Das Poster präsentiert die wichtigsten Ergebnisse der GARCH-Volatilitätsanalyse des S&P 500:

### Hauptabschnitte

1. **Motivation**
   - Warum ist Volatilitätsprognose wichtig?
   - Anwendungsfälle für GARCH-Modelle

2. **Datenanalyse S&P 500**
   - Zeitraum: 04.01.2010 - 20.12.2024
   - 617.631 Beobachtungen
   - Fehlende Werte: 67,34%

3. **ARCH und GARCH in der Zeitreihenanalyse**
   - ARCH (Engle 1982): Autoregressive Conditional Heteroskedasticity
   - GARCH (Bollerslev 1986): Generalized ARCH
   - Modellierung zeitlich variabler bedingter Varianzen

4. **Modelle**
   - **GARCH(1,1)**: Symmetrisches Standardmodell
   - **EGARCH**: Exponential GARCH mit Leverage-Effekt
   - **GJR-GARCH**: Asymmetrische Reaktion auf negative Schocks

5. **Fehlermaß der Volatilitätsprognosen**
   - Mean Squared Error (MSE)
   - Mean Absolute Error (MAE)
   - Vergleich mit Baseline (durchschnittliche Varianz)

6. **Fazit**
   - EGARCH: Beste MAE (0,715)
   - GARCH(1,1): Zweitbester MSE (1,179)
   - GJR-GARCH: Ausgeglichene Performance (MSE 1,188, MAE 0,713)

## 📚 Weitere Dokumentation

Für weitere Informationen siehe:
- [README.md](../README.md) - Hauptdokumentation

## 🎓 Akademischer Kontext

**Kurs:** Diskrete Mathematik und Stochastik - WS 25/26  
**Dozent:** Prof. Dr. Marina Arendt  
**Autoren:** Veit Wetzel, Mauritz Langer  
**Institution:** [Ihre Universität]  
**Veranstaltung:** DSE 2024 (Data Science Event)

## 📖 Zitation

Falls Sie dieses Projekt in Ihrer Arbeit zitieren möchten:

```bibtex
@misc{langer2026garch,
  title={S\&P 500 Volatilitätsprognose: Ein Vergleich von GARCH-Modellen},
  author={Langer, Mauritz and Wetzel, Veit},
  year={2026},
  note={Diskrete Mathematik und Stochastik - WS 25/26}
}
```

## 🔗 Verwandte Literatur

Die vollständige Literaturliste finden Sie in [DMS.bib](../DMS.bib).

Wichtigste Quellen:
- Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity
- Engle, R. F. (1982). Autoregressive Conditional Heteroscedasticity
- Mustapa & Ismail (2019). Modelling and forecasting S&P 500 stock prices using hybrid Arima-Garch Model

---

**Letzte Aktualisierung:** Januar 2026
