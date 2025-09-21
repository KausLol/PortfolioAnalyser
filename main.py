import yfinance as yf
import pandas as pd
import asyncio
import time


def read_portfolio():
    df = pd.read_csv("portfolio.csv", names=['ticker', 'quantity'])

    print("Portfolio:")
    print(df)
    print("\n" + "=" * 50 + "\n")

    return df


async def fetch_stock(symbol, quantity):
    stock = yf.Ticker(symbol)
    info = stock.info
    
    current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    company_name = info.get('longName', symbol)
    
    position_value = current_price * quantity
    
    print(f"{symbol} ({company_name})")
    print(f"  Shares: {quantity}")
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Position Value: ${position_value:.2f}")
    print("-" * 40)
    
    return position_value


async def calculate_portfolio_value(dataFrame):
    total_value = 0
    tasks = []
    
    # tasks for each stock
    for index, row in dataFrame.iterrows():
        symbol = row['ticker']
        quantity = row['quantity']
        task = asyncio.create_task(fetch_stock(symbol, quantity))
        tasks.append(task)
    
    # wait for all tasks, then sum values
    for task in tasks:
        position_value = await task
        total_value += position_value

    print(f"\nTotal Portfolio Value: ${total_value:.2f}")


async def main():
    start_time = time.time()
    
    data = read_portfolio()
    await calculate_portfolio_value(data)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nExecution Time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
