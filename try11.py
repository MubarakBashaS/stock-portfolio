import requests

key = 'YOUR_ALPHA_VANTAGE_API_KEY'
url = 'https://www.alphavantage.co/query'

portfolio = {}

def get_stock_price(sym):
    """Fetch the current stock price from Alpha Vantage."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': sym,
        'interval': '1min',
        'apikey': key
    }
    try:
        response = requests.get(url , params=params)
        response.raise_for_status()  
        data = response.json()
        if 'Time Series (1min)' in data:
            latest_time = list(data['Time Series (1min)'].keys())[0]
            latest_price = data['Time Series (1min)'][latest_time]['1. open']
            return float(latest_price)
        else:
            print(f"Error: {data.get('Error Message', 'Unable to fetch data')}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def add_stock(sym, quantity):
    """Add or update a stock in the portfolio."""
    sym = sym.upper()
    price = get_stock_price(sym)
    if price is not None:
        if sym in portfolio:
            portfolio[sym]['quantity'] += quantity
        else:
            portfolio[sym] = {'quantity': quantity, 'price': price}
        print(f"Added {quantity} of {sym} to the portfolio.")
    else:
        print("Failed to add stock. Price data unavailable.")

def remove_stock(sym, quantity):
    """Remove or update a stock from the portfolio."""
    sym = sym.upper()
    if sym in portfolio:
        if portfolio[sym]['quantity'] >= quantity:
            portfolio[sym]['quantity'] -= quantity
            if portfolio[sym]['quantity'] == 0:
                del portfolio[sym]
            print(f"Removed {quantity} of {sym} from the portfolio.")
        else:
            print("Insufficient quantity to remove.")
    else:
        print("Stock not found in portfolio.")

def print_portfolio():
    """Print the current portfolio."""
    if not portfolio:
        print("Portfolio is empty.")
        return
    for sym, data in portfolio.items():
        print(f"{sym}: Quantity = {data['quantity']}, Price = ${data['price']:.2f}")

def calculate_performance():
    """Calculate and print the total value of the portfolio."""
    total_value = 0
    for sym, data in portfolio.items():
        price = get_stock_price(sym)
        if price is not None:
            total_value += price * data['quantity']
        else:
            print(f"Warning: Unable to fetch price for {sym}")
    print(f"Total portfolio value: ${total_value:.2f}")

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Calculate Performance")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            sym = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            add_stock(sym, quantity)
        
        elif choice == '2':
            sym = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            remove_stock(sym, quantity)
        
        elif choice == '3':
            print_portfolio()
        
        elif choice == '4':
            calculate_performance()
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
