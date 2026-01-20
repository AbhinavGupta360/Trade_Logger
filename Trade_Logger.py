import pandas as pd
from datetime import datetime
import os

FILE = "Trade_Logger/trades.csv"
COLUMNS = ["Date", "Strategy", "Symbol", "Entry", "Exit", "Qty", "Type", "PnL"]

def load_trades():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=COLUMNS)

def log_trade(df):
    strategy = input("Strategy Name: ").strip().upper()
    symbol = input("Symbol: ").strip().upper()
    entry = float(input("Entry Price: "))
    exit = float(input("Exit Price: "))
    qty = int(input("Quantity: "))
    trade_type = input("Type (BUY/SELL): ").upper()

    pnl = (exit - entry) * qty if trade_type == "BUY" else (entry - exit) * qty

    trade = pd.DataFrame([{
        "Date": datetime.now(),
        "Strategy": strategy,
        "Symbol": symbol,
        "Entry": entry,
        "Exit": exit,
        "Qty": qty,
        "Type": trade_type,
        "PnL": pnl
    }])

    df = pd.concat([df, trade], ignore_index=True)
    df.to_csv(FILE, index=False)
    return df

def analyze_trades(df):
    print("\n OVERALL ANALYSIS")
    print("-" * 40)

    df = df.sort_values("Date")

    equity = df["PnL"].cumsum()
    print("Total Trades :", len(df))
    print("Total PnL    :", round(df["PnL"].sum(), 2))
    print("Win Rate    :", round((df["PnL"] > 0).mean() * 100, 2), "%")
    print("Max Drawdown:", round((equity - equity.cummax()).min(), 2))
    print("Avg PnL     :", round(df["PnL"].mean(), 2))

    wins = df[df["PnL"] > 0]["PnL"].mean()
    losses = df[df["PnL"] < 0]["PnL"].mean()
    expectancy = (wins * (df["PnL"] > 0).mean()) + (losses * (df["PnL"] < 0).mean())
    print("Expectancy :", round(expectancy, 2))

    print("\n STRATEGY-WISE ANALYSIS")
    print("-" * 40)

    grouped = df.groupby("Strategy")

    for strategy, s_df in grouped:
        equity = s_df["PnL"].cumsum()
        print(f"\nStrategy: {strategy}")
        print("Trades       :", len(s_df))
        print("Total PnL    :", round(s_df["PnL"].sum(), 2))
        print("Win Rate    :", round((s_df["PnL"] > 0).mean() * 100, 2), "%")
        print("Max Drawdown:", round((equity - equity.cummax()).min(), 2))
        print("Avg PnL     :", round(s_df["PnL"].mean(), 2))

def main():
    df = load_trades()

    while True:
        print("\n CURRENT TRADES (Last 10)")
        print(df.tail(10) if not df.empty else "No trades logged yet.")

        choice = input("\nLog a new trade? (yes/no): ").lower()
        if choice != "yes":
            break

        df = log_trade(df)

    if not df.empty:
        analyze_trades(df)
    else:
        print("No trades to analyze.")

if __name__ == "__main__":
    main()


