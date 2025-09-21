import yfinance as yf
import pandas as pd
import asyncio


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
    print("  d) Display & evaluate sample portfolio")
    print("  q) Quit")
    print()
    print("-" * 50)
    
    # exception handling
    try:
        choice = input("Enter your choice (a/b/c/d/q): ").lower().strip()
        print()
        return choice
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        return 'q'
    except EOFError:
        print("\n\nInput stream closed.")
        return 'q' 
    except Exception as e:
        # tells the user about a specific error
        print(f"\nError reading input: {e}")
        # return empty string to trigger invalid choice message
        return ''


# read csv file as a whole
def read_portfolio():
    try:
        df = pd.read_csv("portfolio.csv", names=['ticker', 'quantity'])
        
        # Check if CSV is empty
        if df.empty:
            print("Portfolio is empty!")
            print("Use option 'a' to add entries to your portfolio.")
            print("\n" + "=" * 50 + "\n")
            return None
        
        print("Portfolio:")
        print(df)
        print("\n" + "=" * 50 + "\n")
        return df
        
    # exception handling
    except FileNotFoundError:
        print("Portfolio file not found!")
        print("Use option 'a' to create your first portfolio entry.")
        print("\n" + "=" * 50 + "\n")
        return None
    except Exception as e:
        print(f"Error reading portfolio: {e}")
        print("Please check your portfolio.csv file.")
        print("\n" + "=" * 50 + "\n")
        return None


def read_sample_portfolio():
    try:
        df = pd.read_csv("sample.csv", names=['ticker', 'quantity'])
        
        # checks if CSV is empty
        if df.empty:
            print("Sample portfolio is empty!")
            print("\n" + "=" * 50 + "\n")
            return None
        
        print("Sample Portfolio:")
        print(df)
        print("\n" + "=" * 50 + "\n")
        return df

    # exception handling  
    except FileNotFoundError:
        print("Sample portfolio file (sample.csv) not found!")
        print("Please make sure sample.csv exists in the directory.")
        print("\n" + "=" * 50 + "\n")
        return None
    except Exception as e:
        print(f"Error reading sample portfolio: {e}")
        print("Please check your sample.csv file.")
        print("\n" + "=" * 50 + "\n")
        return None


# append entries to the csv file
def write_csv():
    while True:
        try:
            user_input = input("Write symbol and quantity separated by space. "
            "(Press Q to go back to menu): ")

            if user_input.strip().lower() == "q":
                # quit appending
                return
            
            # Check if input is empty
            if not user_input.strip():
                print("Error: Please enter a symbol and quantity.")
                continue
            
            # split symbol and quantity as list items
            split_input = user_input.split(" ")
            
            # Check if user entered exactly 2 values
            if len(split_input) != 2:
                print("Error: Please enter exactly one symbol and one quantity separated by space.")
                print("Example: AAPL 50")
                continue
            
            symbol = split_input[0].upper()  # Convert to uppercase
            quantity_str = split_input[1]
            
            # Check if quantity is a valid number
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    print("Error: Quantity must be a positive number.")
                    continue
            except ValueError:
                print("Error: Quantity must be a valid number.")
                continue
            
            data["quantity"].append(quantity)
            data["symbol"].append(symbol)

            # convert to DataFrame and append to CSV
            df = pd.DataFrame({"ticker": [symbol], "quantity": [quantity]})
            df.to_csv('portfolio.csv', mode='a', header=False, index=False)
            
            print(f"Added {symbol}: {quantity} shares to portfolio.")
            
        except PermissionError:
            print("Error: Cannot write to portfolio.csv - file may be open in another program.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")


# to clear all the entries in the csv file
def clear_csv():
    try:
        confirm = input("Are you sure you want to clear your entire portfolio? (y/n): ").lower().strip()
        
        if confirm == 'y' or confirm == 'yes':
            # overwrite existing file with empty dataframe
            empty_df = pd.DataFrame()
            empty_df.to_csv("portfolio.csv", index=False)
            print("Portfolio cleared successfully!")
        else:
            print("Portfolio clear cancelled.")
            
    # exception handling
    except PermissionError:
        print("Error: Cannot clear portfolio.")
    except Exception as e:
        print(f"Error clearing portfolio: {e}")
        print("Please try again.")


# get data from yfinance
async def fetch_stock(symbol, quantity):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # check if we got valid data
        if not info or 'currentPrice' not in info and 'regularMarketPrice' not in info:
            print(f"{symbol} - Error: Invalid symbol or no price data available")
            print(f"  Shares: {quantity}")
            print(f"  Current Price: N/A")
            print(f"  Position Value: N/A")
            print("-" * 40)
            return 0  # return 0 for failed stocks
        
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        company_name = info.get('longName', symbol)
        
        # check if price is valid
        if current_price == 0:
            print(f"{symbol} ({company_name}) - Error: No price data available")
            print(f"  Shares: {quantity}")
            print(f"  Current Price: N/A")
            print(f"  Position Value: N/A")
            print("-" * 40)
            return 0
        
        position_value = current_price * quantity
        
        print(f"{symbol} ({company_name})")
        print(f"  Shares: {quantity}")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  Position Value: ${position_value:.2f}")
        print("-" * 40)
        
        return position_value
        
    except Exception as e:
        print(f"{symbol} - Error fetching data: {e}")
        print(f"  Shares: {quantity}")
        print(f"  Current Price: N/A")
        print(f"  Position Value: N/A")
        print("-" * 40)
        return 0  # Return 0 for failed stocks


# calculate portfolio value
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
    try:
        while True:
            choice = display_menu()
            
            if choice == 'a':
                write_csv()
            elif choice == 'b':
                data = read_portfolio()

                # proceeds only if some data exists
                if data is not None:
                    await calculate_portfolio_value(data)
            elif choice == "c":
                clear_csv()
            elif choice == "d":
                sample_data = read_sample_portfolio()
                if sample_data is not None:
                    await calculate_portfolio_value(sample_data)
            elif choice == 'q':
                print("Thank you for using Portfolio Analyzer!")
                print("=" * 50)
                break
            else:
                print("Invalid choice. Please select 'a', 'b', 'c', 'd', or 'q'.")
                print("-" * 40)
            
            print("\n")
            
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("The program will now exit.")


if __name__ == "__main__":
    # exception handling
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye!")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please make sure all required packages are installed:")
        print("pip install yfinance pandas")
    except Exception as e:
        print(f"Critical error: {e}")
        print("The program encountered an unexpected error and will now exit.")
