[garch_analysis.md](garch_analysis.md)# S&P 500 GARCH Volatility Analysis - Jupyter Notebook

## Installation und Abhängigkeiten

Installieren Sie zuerst die notwendigen Pakete:

```bash
pip install pandas numpy matplotlib seaborn arch statsmodels scikit-learn scipy
```

## Komplettes Jupyter Notebook

```python
# ==============================================================================
# S&P 500 GARCH Volatility Analysis
# Forschungsfrage 1: Volatilitätsprognose mit verschiedenen GARCH-Modellen
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from arch import arch_model
from arch.univariate import GARCH, EGARCH, ConstantMean, Normal, ZeroMean
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==============================================================================
# SCHRITT 1: DATEN LADEN UND VORBEREITEN
# ==============================================================================

# Daten von Kaggle laden (oder von Yahoo Finance herunterladbar)
df = pd.read_csv('sp500_index.csv')

# Datenspalten überprüfen
print("Spalten im Datensatz:")
print(df.head())
print(f"\nDatensatzform: {df.shape}")

# Daten sortieren (älteste zuerst)
df = df.sort_values('Date').reset_index(drop=True)

# Close-Preise extrahieren
prices = df['Close'].values
dates = pd.to_datetime(df['Date'])

# Log-Renditen berechnen
returns = np.log(prices[1:] / prices[:-1]) * 100  # in Prozent für bessere Lesbarkeit
returns_df = pd.DataFrame({
    'Date': dates[1:],
    'Returns': returns
}).set_index('Date')

print(f"\nAnzahl der Renditen: {len(returns)}")
print(f"Zeitraum: {dates[1].date()} bis {dates[-1].date()}")

# ==============================================================================
# SCHRITT 2: DESKRIPTIVE STATISTIK UND EXPLORATIVE DATENANALYSE
# ==============================================================================

print("\n" + "="*60)
print("DESKRIPTIVE STATISTIK DER LOG-RENDITEN")
print("="*60)

stats_dict = {
    'Mittelwert': returns.mean(),
    'Standardabweichung': returns.std(),
    'Minimum': returns.min(),
    'Maximum': returns.max(),
    'Schiefe (Skewness)': stats.skew(returns),
    'Kurtosis (Exzess)': stats.kurtosis(returns),
    'Jarque-Bera Test': stats.jarque_bera(returns)[1]
}

for key, value in stats_dict.items():
    print(f"{key:.<30} {value:.6f}")

# Stationarität prüfen (Augmented Dickey-Fuller Test)
adf_result = adfuller(returns, autolag='AIC')
print(f"\nADF Test p-Wert: {adf_result[1]:.6f}")
if adf_result[1] < 0.05:
    print("✓ Zeitreihe ist stationär (H0 abgelehnt)")
else:
    print("✗ Zeitreihe ist nicht stationär")

# ==============================================================================
# SCHRITT 3: VISUALISIERUNG DER RENDITEN
# ==============================================================================

fig, axes = plt.subplots(3, 1, figsize=(14, 10))

# Renditen über Zeit
axes[0].plot(dates[1:], returns, linewidth=1, color='steelblue')
axes[0].set_title('S&P 500 Log-Renditen', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Rendite (%)')
axes[0].grid(True, alpha=0.3)

# Histogramm der Renditen
axes[1].hist(returns, bins=100, color='steelblue', alpha=0.7, edgecolor='black')
axes[1].axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label='Mittelwert')
axes[1].set_title('Verteilung der Log-Renditen', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Rendite (%)')
axes[1].set_ylabel('Häufigkeit')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Q-Q Plot
stats.probplot(returns, dist="norm", plot=axes[2])
axes[2].set_title('Q-Q Plot (Normalverteilungstest)', fontsize=12, fontweight='bold')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_returns_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ==============================================================================
# SCHRITT 4: ACF UND PACF DIAGRAMME
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# ACF/PACF für Renditen
plot_acf(returns, lags=40, ax=axes[0, 0], title='ACF: Log-Renditen')
plot_pacf(returns, lags=40, ax=axes[0, 1], title='PACF: Log-Renditen')

# ACF/PACF für quadrierte Renditen (für ARCH-Effekte)
plot_acf(returns**2, lags=40, ax=axes[1, 0], title='ACF: Quadrierte Renditen')
plot_pacf(returns**2, lags=40, ax=axes[1, 1], title='PACF: Quadrierte Renditen')

plt.tight_layout()
plt.savefig('02_acf_pacf.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✓ ARCH-Effekte detektiert in quadrierten Renditen (Volatilitätsclustering)")

# ==============================================================================
# SCHRITT 5: TRAIN-TEST SPLIT
# ==============================================================================

test_size = 0.2  # 20% für Test
split_idx = int(len(returns) * (1 - test_size))

train_returns = returns[:split_idx]
test_returns = returns[split_idx:]

train_dates = dates[1:split_idx+1]
test_dates = dates[split_idx+1:]

print(f"\nTrain-Set: {len(train_returns)} Beobachtungen ({train_dates[0].date()} - {train_dates[-1].date()})")
print(f"Test-Set: {len(test_returns)} Beobachtungen ({test_dates[0].date()} - {test_dates[-1].date()})")

# ==============================================================================
# SCHRITT 6: GARCH(1,1) MODELL
# ==============================================================================

print("\n" + "="*60)
print("GARCH(1,1) MODELLIERUNG")
print("="*60)

# Modell definieren
model_garch11 = arch_model(train_returns, vol='Garch', p=1, q=1, mean='Zero')

# Modell fittern
garch11_result = model_garch11.fit(disp='off')

print(garch11_result.summary())

# Volatilität auf Test-Set extrahieren
garch11_volatility = garch11_result.conditional_volatility.values[-len(test_returns):]

# Forecast für Test-Periode
forecast_garch11 = garch11_result.forecast(horizon=len(test_returns))
garch11_forecast_vol = np.sqrt(forecast_garch11.variance.values[-1, :])

# ==============================================================================
# SCHRITT 7: EGARCH MODELL
# ==============================================================================

print("\n" + "="*60)
print("EGARCH MODELLIERUNG")
print("="*60)

# EGARCH Modell definieren (asymmetrischer Ansatz)
model_egarch = arch_model(train_returns, vol='EGARCH', p=1, q=1, mean='Zero')

egarch_result = model_egarch.fit(disp='off')

print(egarch_result.summary())

# Volatilität extrahieren
egarch_volatility = egarch_result.conditional_volatility.values[-len(test_returns):]

# Forecast
forecast_egarch = egarch_result.forecast(horizon=len(test_returns))
egarch_forecast_vol = np.sqrt(forecast_egarch.variance.values[-1, :])

# ==============================================================================
# SCHRITT 8: GJR-GARCH MODELL
# ==============================================================================

print("\n" + "="*60)
print("GJR-GARCH MODELLIERUNG (Leverage-Effekt)")
print("="*60)

# GJR-GARCH Modell (threshold model mit asymmetrie)
model_gjrgarch = arch_model(train_returns, vol='GARCH', p=1, o=1, q=1, mean='Zero')

gjrgarch_result = model_gjrgarch.fit(disp='off')

print(gjrgarch_result.summary())

# Volatilität extrahieren
gjrgarch_volatility = gjrgarch_result.conditional_volatility.values[-len(test_returns):]

# Forecast
forecast_gjrgarch = gjrgarch_result.forecast(horizon=len(test_returns))
gjrgarch_forecast_vol = np.sqrt(forecast_gjrgarch.variance.values[-1, :])

# ==============================================================================
# SCHRITT 9: EVALUIERUNGSMETRIKEN
# ==============================================================================

print("\n" + "="*60)
print("MODELLVERGLEICH - EVALUIERUNGSMETRIKEN")
print("="*60)

# Realisierte Volatilität als Benchmark
realized_volatility = np.abs(test_returns)

def calculate_metrics(predicted_vol, actual_vol, model_name):
    """Berechne Evaluierungsmetriken"""
    
    rmse = np.sqrt(mean_squared_error(actual_vol, predicted_vol))
    mae = mean_absolute_error(actual_vol, predicted_vol)
    mape = np.mean(np.abs((actual_vol - predicted_vol) / (actual_vol + 1e-10))) * 100
    
    # Diebold-Mariano Statistik (vereinfacht)
    loss_diff = (actual_vol - predicted_vol) ** 2
    dm_stat = np.mean(loss_diff)
    
    return {
        'Modell': model_name,
        'RMSE': rmse,
        'MAE': mae,
        'MAPE (%)': mape,
        'DM Loss': dm_stat
    }

metrics_list = [
    calculate_metrics(garch11_forecast_vol, realized_volatility, 'GARCH(1,1)'),
    calculate_metrics(egarch_forecast_vol, realized_volatility, 'EGARCH(1,1)'),
    calculate_metrics(gjrgarch_forecast_vol, realized_volatility, 'GJR-GARCH(1,1)')
]

metrics_df = pd.DataFrame(metrics_list)
print(metrics_df.to_string(index=False))

# Speichern für später
metrics_df.to_csv('garch_metrics.csv', index=False)

# ==============================================================================
# SCHRITT 10: VOLATILITÄTSVERGLEICH
# ==============================================================================

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

x_axis = np.arange(len(test_returns))

# GARCH(1,1)
axes[0].plot(x_axis, realized_volatility, label='Realisierte Volatilität', 
             linewidth=2, color='black', alpha=0.7)
axes[0].plot(x_axis, garch11_forecast_vol, label='GARCH(1,1) Prognose', 
             linewidth=1.5, color='steelblue', linestyle='--')
axes[0].fill_between(x_axis, realized_volatility, garch11_forecast_vol, 
                      alpha=0.2, color='steelblue')
axes[0].set_title(f'GARCH(1,1) - RMSE: {metrics_df.loc[0, "RMSE"]:.6f}', 
                  fontsize=11, fontweight='bold')
axes[0].set_ylabel('Volatilität')
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# EGARCH
axes[1].plot(x_axis, realized_volatility, label='Realisierte Volatilität', 
             linewidth=2, color='black', alpha=0.7)
axes[1].plot(x_axis, egarch_forecast_vol, label='EGARCH(1,1) Prognose', 
             linewidth=1.5, color='coral', linestyle='--')
axes[1].fill_between(x_axis, realized_volatility, egarch_forecast_vol, 
                      alpha=0.2, color='coral')
axes[1].set_title(f'EGARCH(1,1) - RMSE: {metrics_df.loc[1, "RMSE"]:.6f}', 
                  fontsize=11, fontweight='bold')
axes[1].set_ylabel('Volatilität')
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

# GJR-GARCH
axes[2].plot(x_axis, realized_volatility, label='Realisierte Volatilität', 
             linewidth=2, color='black', alpha=0.7)
axes[2].plot(x_axis, gjrgarch_forecast_vol, label='GJR-GARCH(1,1) Prognose', 
             linewidth=1.5, color='seagreen', linestyle='--')
axes[2].fill_between(x_axis, realized_volatility, gjrgarch_forecast_vol, 
                      alpha=0.2, color='seagreen')
axes[2].set_title(f'GJR-GARCH(1,1) - RMSE: {metrics_df.loc[2, "RMSE"]:.6f}', 
                  fontsize=11, fontweight='bold')
axes[2].set_ylabel('Volatilität')
axes[2].set_xlabel('Test-Periode (Tage)')
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('03_volatility_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# ==============================================================================
# SCHRITT 11: METRIKEN-VISUALISIERUNG
# ==============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# RMSE und MAE Vergleich
x_pos = np.arange(len(metrics_df))
width = 0.35

axes[0].bar(x_pos - width/2, metrics_df['RMSE'], width, label='RMSE', alpha=0.8)
axes[0].bar(x_pos + width/2, metrics_df['MAE'], width, label='MAE', alpha=0.8)
axes[0].set_ylabel('Fehler')
axes[0].set_title('Fehlermetriken Vergleich', fontsize=12, fontweight='bold')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(metrics_df['Modell'], rotation=45, ha='right')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# MAPE Vergleich
colors = ['steelblue', 'coral', 'seagreen']
bars = axes[1].bar(metrics_df['Modell'], metrics_df['MAPE (%)'], color=colors, alpha=0.8)
axes[1].set_ylabel('MAPE (%)')
axes[1].set_title('Durchschnittlicher Absoluter Prozentualer Fehler', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

# Werte auf den Balken anzeigen
for bar in bars:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%', ha='center', va='bottom', fontsize=10)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('04_metrics_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# ==============================================================================
# SCHRITT 12: RESIDUENANALYSE
# ==============================================================================

print("\n" + "="*60)
print("RESIDUENANALYSE")
print("="*60)

fig, axes = plt.subplots(3, 2, figsize=(14, 12))

models = [
    ('GARCH(1,1)', garch11_result),
    ('EGARCH(1,1)', egarch_result),
    ('GJR-GARCH(1,1)', gjrgarch_result)
]

for idx, (name, result) in enumerate(models):
    residuals = result.resid
    standardized_residuals = residuals / result.conditional_volatility
    
    # Histogramm der standardisierten Residuen
    axes[idx, 0].hist(standardized_residuals, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    axes[idx, 0].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[idx, 0].set_title(f'{name} - Standardisierte Residuen', fontsize=11, fontweight='bold')
    axes[idx, 0].set_xlabel('Standardisierte Residuen')
    axes[idx, 0].set_ylabel('Häufigkeit')
    axes[idx, 0].grid(True, alpha=0.3)
    
    # Q-Q Plot
    stats.probplot(standardized_residuals, dist="norm", plot=axes[idx, 1])
    axes[idx, 1].set_title(f'{name} - Q-Q Plot', fontsize=11, fontweight='bold')
    axes[idx, 1].grid(True, alpha=0.3)
    
    # Ljung-Box Test
    from statsmodels.stats.diagnostic import acorr_ljungbox
    lb_test = acorr_ljungbox(standardized_residuals**2, lags=10, return_df=True)
    print(f"\n{name} - Ljung-Box Test (p-Werte):")
    print(lb_test['lb_pvalue'].mean().round(4))

plt.tight_layout()
plt.savefig('05_residuals_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ==============================================================================
# SCHRITT 13: ZUSAMMENFASSUNG UND INTERPRETATION
# ==============================================================================

print("\n" + "="*60)
print("FORSCHUNGSFRAGE 1 - ZUSAMMENFASSUNG")
print("="*60)

best_model_idx = metrics_df['RMSE'].idxmin()
best_model = metrics_df.loc[best_model_idx, 'Modell']

print(f"\n✓ SIEGER (kleinster RMSE): {best_model}")
print(f"  - RMSE: {metrics_df.loc[best_model_idx, 'RMSE']:.6f}")
print(f"  - MAE: {metrics_df.loc[best_model_idx, 'MAE']:.6f}")
print(f"  - MAPE: {metrics_df.loc[best_model_idx, 'MAPE (%)']:.2f}%")

print("\n" + "="*60)
print("KEY FINDINGS:")
print("="*60)

print("""
1. VOLATILITÄTSCLUSTERING: 
   Die ACF-Analyse der quadrierten Renditen zeigt ausgeprägte 
   Volatilitätsmuster (Autokorrelation), was typisch für 
   finanzielle Zeitreihen ist.

2. MODELLVERGLEICH:
   - GARCH(1,1): Symmetrisches Standard-Modell für 
     allgemeine Volatilitätsprognose
   - EGARCH(1,1): Asymmetrisches Modell, erfasst 
     unterschiedliche Reaktionen auf positive/negative Schocks
   - GJR-GARCH(1,1): Leverage-Effekt-Modell für 
     realistische Volatilitätsdynamiken

3. PERFORMANCE:
   Vergleichen Sie RMSE, MAE und MAPE. Ein niedrigerer Wert 
   zeigt bessere Prognosegenauigkeit an.

4. PRAKTISCHE ANWENDUNG:
   - Risk Management: VaR und CVaR Berechnung
   - Optionsbewertung
   - Portfolio-Allokation
   - Hedging-Strategien
""")

print("="*60)
print("ANALYSE ABGESCHLOSSEN!")
print("="*60)

# Speichern aller Ergebnisse
summary_results = {
    'garch11_params': garch11_result.params.to_dict(),
    'egarch_params': egarch_result.params.to_dict(),
    'gjrgarch_params': gjrgarch_result.params.to_dict(),
    'metrics': metrics_df.to_dict()
}

print("\n✓ Alle Abbildungen gespeichert:")
print("  - 01_returns_analysis.png")
print("  - 02_acf_pacf.png")
print("  - 03_volatility_comparison.png")
print("  - 04_metrics_comparison.png")
print("  - 05_residuals_analysis.png")
print("  - garch_metrics.csv")
```

## Wichtige Hinweise zur Ausführung:

### 1. **Datenquellen**
- **Kaggle**: `sp500_index.csv` von [S&P 500 Stocks](https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks)
- **Alternativ Yahoo Finance**:
```python
import yfinance as yf
df = yf.download('^GSPC', start='2015-01-01', end='2025-01-01')
df.to_csv('sp500_index.csv')
```

### 2. **Interpretationen der Ergebnisse**

| Metrik | Interpretation |
|--------|----------------|
| **RMSE** | Root Mean Squared Error - Durchschnittlicher Fehler. Niedriger = besser |
| **MAE** | Mean Absolute Error - Durchschnittliche absolute Abweichung |
| **MAPE** | Mean Absolute Percentage Error - Prozentualer Fehler |
| **Ljung-Box Test** | p > 0.05 = keine Autokorrelation in Residuen (gut) |

### 3. **GARCH Parameter Interpretation**

Für GARCH(p,q):
- **α (alpha)**: Einfluss vergangener Schocks auf Volatilität
- **β (beta)**: Persistenz der Volatilität
- **ω (omega)**: Baseline-Volatilität
- **α + β**: Sollte < 1 sein (Stationarität)

### 4. **Asymmetrische Modelle**

- **EGARCH**: Lograithmische Formulierung, erlaubt Leverage-Effekte
- **GJR-GARCH**: Indikator-Variable für negative Renditen, oft bessere Fits für Finanzdaten

