
"""
Stock Span & Trade Analyzer - Main Entry Point
"""

from stock_analyzer import StockAnalyzer

def main():
    analyzer = StockAnalyzer()
    
    print("🏛️  STOCK SPAN & TRADE ANALYZER")
    print("🔍 Advanced Technical Analysis using Data Structures & Algorithms")
    print("📈 Implementing: Stacks, Queues, Sliding Window, Greedy Algorithms")
    
    # Get input from user
    print("\n" + "="*50)
    print("INPUT CONFIGURATION")
    print("="*50)
    
    # Sample data or user input
    use_sample = input("Use sample data? (y/n): ").lower().strip()
    
    if use_sample == 'y':
        prices = [100, 80, 60, 70, 60, 75, 85, 90, 65, 95, 105, 95]
        print(f"Using sample prices: {prices}")
    else:
        try:
            price_input = input("Enter stock prices (comma-separated): ")
            prices = [float(x.strip()) for x in price_input.split(',')]
        except ValueError:
            print("Invalid input. Using sample data.")
            prices = [100, 80, 60, 70, 60, 75, 85, 90, 65, 95, 105, 95]
    
    try:
        window_size = int(input(f"Enter window size for moving average (default 3): ") or "3")
    except ValueError:
        window_size = 3
    
    if len(prices) < 2:
        print("Error: Need at least 2 prices for analysis")
        return
    
    analyzer.prices = prices
    analyzer.window_size = window_size
    
    # Perform all analyses
    print(f"\n🚀 Starting analysis with {len(prices)} price points...")
    
    # 1. Stock Span Analysis (Monotonic Stack)
    spans = analyzer.calculate_stock_span(prices)
    
    # 2. Buy/Sell Signals (Greedy Algorithm)
    signals, total_profit, trades = analyzer.calculate_buy_sell_signals(prices)
    
    # 3. Moving Average (Fixed-Size Queue)
    moving_averages = analyzer.calculate_moving_average(prices, window_size)
    
    # 4. Sliding Window Analysis
    windows = analyzer.sliding_window_analysis(prices, window_size)
    
    # 5. Maximum Profit (Kadane's Algorithm)
    max_profit, buy_day, sell_day = analyzer.calculate_max_profit_kadane(prices)
    
    # 6. Anomaly Detection
    anomalies = analyzer.detect_anomalies(prices, moving_averages)
    
    # 7. Comprehensive Summary
    analyzer.print_summary(prices, total_profit, max_profit, buy_day, sell_day, trades, windows)
    
    print(f"\n✅ Analysis Complete!")
    print("="*80)

if __name__ == "__main__":
    main()