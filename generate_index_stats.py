import csv
from datetime import datetime

# Konfiguration
FILE_PATH = 'sp500_index.csv'
DATE_FORMAT = '%Y-%m-%d'

def calculate_quartiles(data):
    """Berechnet Mittelwert, Q1 (25%) und Q3 (75%)"""
    if not data:
        return 0.0, 0.0, 0.0
    
    n = len(data)
    data.sort()
    
    mean_val = sum(data) / n
    q1 = data[int(n * 0.25)]
    q3 = data[int(n * 0.75)]
    
    return mean_val, q1, q3

def format_stat(name, data, unit=""):
    """Formatiert die Ausgabe für eine Statistikzeile"""
    if not data:
        return f"{name:<30} Nicht verfügbar (fehlt im Datensatz)"
        
    mean, q1, q3 = calculate_quartiles(data)
    return f"{name:<30} {mean:.2f} {unit} [{q1:.2f}; {q3:.2f}]"

def main():
    print(f"Lese Datei '{FILE_PATH}'... Bitte warten.")
    
    dates = []
    close_values = [] # Entspricht der Spalte 'S&P500'
    
    total_rows = 0
    missing_value_rows = 0
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Prüfen welche Spalten da sind (Header)
            # Erwartet: Date, S&P500
            
            for row in reader:
                total_rows += 1
                
                # Datum parsen
                try:
                    current_date = datetime.strptime(row['Date'], DATE_FORMAT)
                except (ValueError, KeyError):
                    continue

                val_str = row.get('S&P500')
                
                if not val_str or not val_str.strip():
                    missing_value_rows += 1
                    continue
                
                try:
                    val = float(val_str)
                    dates.append(current_date)
                    close_values.append(val)
                except ValueError:
                    missing_value_rows += 1
                    continue

    except FileNotFoundError:
        print(f"Fehler: Datei '{FILE_PATH}' nicht gefunden.")
        return

    # --- Berechnungen ---
    
    # 1. Zeitraum
    if dates:
        start_date = min(dates).strftime('%d.%m.%Y')
        end_date = max(dates).strftime('%d.%m.%Y')
        period_str = f"{start_date} – {end_date}"
    else:
        period_str = "Keine gültigen Daten"

    # 2. Fehlende Werte
    missing_percent = (missing_value_rows / total_rows * 100) if total_rows > 0 else 0
    
    # --- Ausgabe ---
    print("\n" + "="*60)
    print(f"{ 'STATISTIK ÜBERSICHT (INDEX)':^60}")
    print("="*60)
    
    print(f"{ 'Beobachtungszeitraum':<30} {period_str}")
    print(f"{ 'Anzahl der Handelstage (N)':<30} {len(dates):,} (Gesamtzeilen: {total_rows:,})".replace(',', '.'))
    print(f"{ 'Fehlende Werte (Gesamt)':<30} {missing_percent:.2f} %")
    print(f"{ 'Vollständige Zeitreihen':<30} 100 % (Index ist eine einzelne Reihe)")
    print("-" * 60)
    # Da nur ein Wert pro Tag existiert (S&P500 Level), mappen wir diesen auf Close
    print(format_stat("Eröffnungskurs (Open)", [])) # Leer
    print(format_stat("Schlusskurs (S&P 500 Value)", close_values, "PKT"))
    print(format_stat("Bereinigter Schlusskurs (Adj)", [])) # Leer
    print(format_stat("Handelsvolumen (Volume)", [])) # Leer
    print(format_stat("Tägliche Volatilität (H-L)", [])) # Leer
    print("="*60)

if __name__ == "__main__":
    main()
