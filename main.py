import yfinance as yf
import pandas as pd
import asyncio


def read():
    df = pd.read_csv("portfolio.csv", names=['ticker', 'quantity'])

    print("Portfolio:")
    print(df)
    print("\n" + "=" * 50 + "\n")

    return df


async def calculate(dataFrame):
    total_value = 0
    for index, row in dataFrame.iterrows():
        symbol = row['ticker']
        quantity = row['quantity']
        
        stock = yf.Ticker(symbol)
        info = stock.info
        
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        company_name = info.get('longName', symbol)
        
        position_value = current_price * quantity
        total_value += position_value
        
        print(f"{symbol} ({company_name})")
        print(f"  Shares: {quantity}")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  Position Value: ${position_value:.2f}")
        print("-" * 40)

    print(f"\nTotal Portfolio Value: ${total_value:.2f}")


async def main():
    # add functionality to write or edit csv
    data = read()
    calculate(data)


if __name__ == "__main__":
    main()
