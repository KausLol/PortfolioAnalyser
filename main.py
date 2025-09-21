import yfinance as yf
import pandas as pd
import asyncio
import time

# empty data for user to add entries
data = {
    "symbol": [],
    "quantity": [],
        }


# function to display a menu
def display_menu():
    print("=" * 50)
    print("           Portfolio Analyser")
    print("=" * 50)
    print()
    print("You can manually edit the 'portfolio.csv' file in the root directory.")
    print()
    print("Please select an option:")
    print()
    print("  a) Write entries in portfolio")
    print("  b) Display & evaluate portfolio")
    print("  c) Clear portfolio")
    print("  q) Quit")
    print()
    print("-" * 50)
    choice = input("Enter your choice (a/b/q): ").lower().strip()
    print()
    return choice


# read csv file as a whole
def read_portfolio():
    df = pd.read_csv("portfolio.csv", names=['ticker', 'quantity'])

    print("Portfolio:")
    print(df)
    print("\n" + "=" * 50 + "\n")

    return df


def write_csv():
    while True:
        user_input = input("Write symbol and quantity separated by space. "
        "(Press Q to go back to menu): ")

        if user_input.strip().lower() == "q":
            # quit appending
            return
        else:
            # split symbol and quanity as list items
            split_input = user_input.split(" ")
            data["quantity"].append(split_input[1])
            data["symbol"].append(split_input[0])

            # convert to DataFrame and append to CSV
            df = pd.DataFrame({"ticker": [split_input[0]], "quantity": [split_input[1]]})
            df.to_csv('portfolio.csv', mode='a', header=False, index=False)


def clear_csv():
    # overwrite existing file with empty dataframe
    empty_df = pd.DataFrame()
    empty_df.to_csv("portfolio.csv", index=False)


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
    while True:
        choice = display_menu()
        
        if choice == 'a':
            write_csv()
        elif choice == 'b':
            data = read_portfolio()
            await calculate_portfolio_value(data)
        elif choice == "c":
            clear_csv()
        
        elif choice == 'q':
            print("Thank you for using Portfolio Analyzer!")
            print("=" * 50)
            break
        else:
            print("Invalid choice. Please select 'a', 'b', or 'q'.")
            print("-" * 40)
        
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
