import csv
from datetime import datetime
import math

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

def format_stat(name, data, unit="", is_volume=False):
    """Formatiert die Ausgabe für eine Statistikzeile"""
    mean, q1, q3 = calculate_quartiles(data)
    
    if is_volume:
        # Volumen in Millionen
        return f"{name:<30} {mean/1e6:.2f} Mio. [{q1/1e6:.2f}; {q3/1e6:.2f}]"
    else:
        return f"{name:<30} {mean:.2f} {unit} [{q1:.2f}; {q3:.2f}]"

def main():
    print(f"Lese Datei '{FILE_PATH}'... Bitte warten.")
    
    # Datenspeicher
    dates = []
    opens = []
    closes = []
    adj_closes = []
    volumes = []
    volatilities = [] # High - Low
    
    # Ticker Tracking für Zeitreihen-Analyse
    ticker_dates = {}
    
    # Zähler
    total_rows = 0
    valid_rows = 0
    missing_value_rows = 0
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                total_rows += 1
                
                # Datum parsen
                try:
                    current_date = datetime.strptime(row['Date'], DATE_FORMAT)
                except (ValueError, KeyError):
                    continue # Überspringe Zeilen ohne gültiges Datum

                symbol = row.get('Symbol')
                
                # Datencheck: Sind alle benötigten Werte vorhanden und nicht leer?
                required_fields = ['Open', 'Close', 'Adj Close', 'Volume', 'High', 'Low']
                if not all(row.get(field) and row.get(field).strip() for field in required_fields):
                    missing_value_rows += 1
                    continue
                
                try:
                    # Werte konvertieren
                    o = float(row['Open'])
                    c = float(row['Close'])
                    ac = float(row['Adj Close'])
                    v = float(row['Volume'])
                    h = float(row['High'])
                    l = float(row['Low'])
                    
                    # Speichern
                    dates.append(current_date)
                    opens.append(o)
                    closes.append(c)
                    adj_closes.append(ac)
                    volumes.append(v)
                    volatilities.append(h - l)
                    
                    # Ticker Zeitspanne tracken
                    if symbol:
                        if symbol not in ticker_dates:
                            ticker_dates[symbol] = {'min': current_date, 'max': current_date}
                        else:
                            if current_date < ticker_dates[symbol]['min']:
                                ticker_dates[symbol]['min'] = current_date
                            if current_date > ticker_dates[symbol]['max']:
                                ticker_dates[symbol]['max'] = current_date
                                
                    valid_rows += 1
                    
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

    # 2. Fehlende Werte (Prozent)
    missing_percent = (missing_value_rows / total_rows * 100) if total_rows > 0 else 0
    
    # 3. Vollständige Zeitreihen > 10 Jahre
    # 10 Jahre = 365 * 10 Tage (grob)
    tickers_over_10y = 0
    total_tickers = len(ticker_dates)
    
    for t_data in ticker_dates.values():
        duration = (t_data['max'] - t_data['min']).days
        if duration > 3650: # > 10 Jahre
            tickers_over_10y += 1
            
    ticker_percent = (tickers_over_10y / total_tickers * 100) if total_tickers > 0 else 0

    # --- Ausgabe ---
    print("\n" + "="*60)
    print(f"{ 'STATISTIK ÜBERSICHT':^60}")
    print("="*60)
    
    print(f"{ 'Beobachtungszeitraum':<30} {period_str}")
    print(f"{ 'Anzahl der Handelstage (N)':<30} {valid_rows:,} (Gesamtzeilen: {total_rows:,})".replace(',', '.'))
    print(f"{ 'Fehlende Werte (Gesamt)':<30} {missing_percent:.2f} %")
    print(f"{ 'Vollständige Zeitreihen (>10J)':<30} {ticker_percent:.1f} % der Ticker ({tickers_over_10y}/{total_tickers})")
    print("-" * 60)
    print(format_stat("Eröffnungskurs (Open)", opens, "$"))
    print(format_stat("Schlusskurs (Close)", closes, "$"))
    print(format_stat("Bereinigter Schlusskurs (Adj)", adj_closes, "$"))
    print(format_stat("Handelsvolumen (Volume)", volumes, "", is_volume=True))
    print(format_stat("Tägliche Volatilität (H-L)", volatilities, "$"))
    print("="*60)

if __name__ == "__main__":
    main()
